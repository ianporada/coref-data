"""
Write the raw gum dataset to the HuggingFace Hub.

Uploads universal dependencies, universal coreference, and OntoNotes style coreference chains.

Uses the published splits. Bridging anaphora is not yet fully parsed
"""

import copy
import glob
import os
import re

from conll_coref_transform import conll_transform
from datasets import Dataset, DatasetDict
from stanza.utils.conll import FIELD_TO_IDX, CoNLL
from udapi.block.read.conllu import Conllu as ConlluReader

GUM_CONLLU_DIR = "dep/"
GUM_CONLL_DIR = "coref/gum/conll/"

ONTOGUM_CONLLU_DIR = "coref/ontogum/conllu/"
ONTOGUM_CONLL_DIR = "coref/ontogum/conll/"

CONLLU_TEXT_COL = FIELD_TO_IDX["text"]
IDX_TO_FIELD = {v:k for k, v in FIELD_TO_IDX.items()}

RAW_DEV_IDS = """
  * GUM_academic_exposure
  * GUM_academic_librarians
  * GUM_bio_byron
  * GUM_bio_emperor
  * GUM_conversation_grounded
  * GUM_conversation_risk
  * GUM_fiction_beast
  * GUM_fiction_lunre
  * GUM_interview_cyclone
  * GUM_interview_gaming
  * GUM_news_homeopathic
  * GUM_news_iodine
  * GUM_reddit_macroeconomics
  * GUM_reddit_pandas
  * GUM_speech_impeachment
  * GUM_speech_inauguration
  * GUM_textbook_governments
  * GUM_textbook_labor
  * GUM_vlog_portland
  * GUM_vlog_radiology
  * GUM_voyage_athens
  * GUM_voyage_coron
  * GUM_whow_joke
  * GUM_whow_overalls
"""

RAW_TEST_IDS = """
  * GUM_academic_discrimination
  * GUM_academic_eegimaa
  * GUM_bio_dvorak
  * GUM_bio_jespersen
  * GUM_conversation_lambada
  * GUM_conversation_retirement
  * GUM_fiction_falling
  * GUM_fiction_teeth
  * GUM_interview_hill
  * GUM_interview_libertarian
  * GUM_news_nasa
  * GUM_news_sensitive
  * GUM_reddit_escape
  * GUM_reddit_monsters
  * GUM_speech_austria
  * GUM_speech_newzealand
  * GUM_textbook_chemistry
  * GUM_textbook_union
  * GUM_vlog_london
  * GUM_vlog_studying
  * GUM_voyage_oakland
  * GUM_voyage_vavau
  * GUM_whow_cactus
  * GUM_whow_mice
"""


def parse_list_of_split_ids(raw_list_of_ids):
    return [x.replace("*", "").strip() for x in raw_list_of_ids.split("\n") if x]


def read_ontogum_conll_file(fname):
    """
    Read ontogum conll file
    each row consists of [global_token_id, token, coref_info]
    """
    lines = []
    with open(fname, "r") as f:
        for line in f:
            line = line.rstrip()
            if not line or line.startswith("#"):
                continue
            row = line.split("\t")
            lines.append(row)
    return lines


def compute_ontogum_coref_chains(doc_dict, raw_ontogum_lines):
    ontogum_doc_dict = copy.deepcopy(doc_dict)

    doc_as_list = [] # List[List[List]], representing each token in each sentence
    for sentence in ontogum_doc_dict:
        new_sentence = []
        for row in sentence:
            new_row = [row[IDX_TO_FIELD[i]] if IDX_TO_FIELD[i] in row else '_' for i in range(len(IDX_TO_FIELD))]
            new_sentence.append(new_row)
        doc_as_list.append(new_sentence)

    global_token_idx = 0
    for sent in doc_as_list:
        for row in sent:
            raw_ontogum_row = raw_ontogum_lines[global_token_idx]
            global_token_idx += 1
            _, token, coref_info = raw_ontogum_row

            assert row[CONLLU_TEXT_COL] == token, f"Mismatch {row[CONLLU_TEXT_COL]} and {token} at {row[0]}"
            row[-1] = coref_info
    ontogum_coref_chains = conll_transform.compute_chains(doc_as_list)
    return ontogum_doc_dict, ontogum_coref_chains


def read_corefud_data(conllu_fname):
    """
    Read sentence metadata and corefud annotations
    """
    docs = ConlluReader(files=conllu_fname, split_docs=True).read_documents()
    assert len(docs) == 1, "GUM should contain one doc per file"
    doc = docs[0]

    sentences = []
    
    for node in doc.nodes_and_empty:

        # assert not node.is_empty(), f"GUM should not have empty nodes: {node} at {node.ord}"
        # nevermind GUM indeed has empty nodes

        if node.ord == 1: # for the first node in the tree, create a new sentence
            root = node.root
            speaker = None
            match = re.search("^ speaker = (.+)", root.comment, re.M)
            if match:
                speaker = match.group(1)
            
            sentence = {
                'sent_id': root.sent_id,
                'text': root.text,
                'newpar': root.newpar,
                'newdoc': root.newdoc,
                'global_entity': root.document.meta.get('global.Entity'),
                'comment': root.comment,
                'speaker': speaker,
                'tokens': [],
            }
            sentences.append(sentence)

        coref_mentions = []
        for mention in set(node.coref_mentions):
            coref_mentions.append({
                'span': mention.span,
                'other': mention.other,
                'eid': mention.entity.eid,
                'eid_or_grp': mention.entity.eid_or_grp,
                'etype': mention.entity.etype,
            })

        token = {
            'index': node.ord,
            'form': node.form,
            'coref_mentions': coref_mentions,
        }
        sentences[-1]['tokens'].append(token)

    return sentences


dev_ids = parse_list_of_split_ids(RAW_DEV_IDS)
test_ids = parse_list_of_split_ids(RAW_TEST_IDS)

docs = []
for conllu_fname in glob.glob(os.path.join(GUM_CONLLU_DIR, "*.conllu")):
    doc_id = os.path.basename(conllu_fname).replace(".conllu", "")
    conll_fname = os.path.join(GUM_CONLL_DIR, doc_id + ".conll")
    ontogum_conll_fname = os.path.join(ONTOGUM_CONLL_DIR, doc_id + ".conll")

    # read the conllu file
    doc = CoNLL.conll2doc(conllu_fname)
    doc_dict = doc.to_dict() # List[List[Dict]], representing each token / word in each sentence

    # filter out multi-token rows
    doc_dict = [[row for row in sent if isinstance(row["id"], int)] for sent in doc_dict]

    # read the ontogum annotations
    raw_ontogum_lines = read_ontogum_conll_file(ontogum_conll_fname)
    ontogum_doc_dict, ontogum_coref_chains = compute_ontogum_coref_chains(doc_dict, raw_ontogum_lines)

    # use udapi to read the corefud annotations from the conllu files
    corefud_sentences = read_corefud_data(conllu_fname)

    # merge doc_dict with corefud_sentences
    merged_sentences = []
    for sent_idx, sent in enumerate(doc_dict):
        corefud_sent = corefud_sentences[sent_idx]

        for token_idx, token_dict in enumerate(sent):
            conllu_token = token_dict["text"]
            corefud_token = corefud_sent["tokens"][token_idx]["form"]
            assert conllu_token == corefud_token, \
                f"Tokens do not match: {conllu_token} and {corefud_token} in {doc_id} at ({sent_idx}, {token_idx})" 

        corefud_sent["conll_rows"] = sent
        merged_sentences.append(corefud_sent)

    doc = {
        "doc_id": doc_id,
        "sentences": merged_sentences,
        "ontogum_sentences": ontogum_doc_dict,
        "ontogum_coref_chains": ontogum_coref_chains,
    }


# # data files are available at this URL
# DATA_URL = "https://github.com/machinereading/CR/blob/743f758e2b0c1fad6a06ce600b59ae882ab66c0e/input/"

# TRAIN_FNAME = "nonJosa_train1345.NER5.v4_gold_conll"
# VALIDATION_FNAME = "nonJosa_dev.NER5.v4_gold_conll"
# TEST_FNAME = "whole.korean8_pd_NER.v4_gold_conll"

# DOC_ID_PATTERN = r"#begin document \((.+)\); part \d+"

# NER_dic = {'PERSON': 0, 'STUDY_FIELD' : 5, 'THEORY' : 5,
#            'ARTIFACTS' : 5, 'ORGANIZATION' : 2, 'LOCATION' : 1,
#            'CIVILIZATION' : 5, 'DATE' : 5, 'TIME': 4,
#            'EVENT' : 3, 'ANIMAL' : 5, 'PLANT' : 5,
#            'MATERIAL' : 5, 'TERM' : 5, 'JOB' : 5,
#            'QUANTITY' : 5, 'ETC' : 5}

# # These are all the columns that are used in the dataset
# # Inferred from https://github.com/machinereading/CR/blob/743f758e2b0c1fad6a06ce600b59ae882ab66c0e/make_conll.py
# TOK_IDX_COL = 2
# LEMMA_COL = 3
# POS_COL = 4
# VERB_STEM_COL = 6
# NER_TYPE_COL = 10
# ZERO_ANAPHORA_INDEX_COL = 11
# COREF_COL = 15


# def read_raw_docs(fname):
#     # map doc_id to list of sentences, each sentence is list of features
#     docs = {}

#     # parse all conll documents into a dict
#     with open(fname, "r") as f:
#         current_doc_id = None
#         for line in f:
#             line = line.rstrip()

#             if line.startswith("#begin document"):
#                 assert current_doc_id is None
#                 full_doc_id = re.search(DOC_ID_PATTERN, line).group(1)
#                 current_doc_id = os.path.basename(full_doc_id)
#                 docs[current_doc_id] = []

#             elif line.startswith("#end document"):
#                 assert current_doc_id is not None
#                 current_doc_id = None
                
#             elif line:
#                 cols = line.split("\t")
#                 token_idx = int(cols[TOK_IDX_COL])
#                 if token_idx == 0:
#                     docs[current_doc_id].append([])
#                 docs[current_doc_id][-1].append(cols)

#     return docs


# def read_formatted_docs_as_list(fname):
#     raw_docs = read_raw_docs(fname)
#     docs = []
#     for doc_id, raw_sentences in raw_docs.items():
#         # Return a list of chains,
#         #     * each being a list of mentions,
#         #     * each being a tuple of (sent, start, end), inclusive
#         chains = conll_transform.compute_chains(raw_sentences)

#         clean_sentences = []
#         for raw_sentence in raw_sentences:
#             clean_sentence = {
#                 "lemmas": [row[LEMMA_COL].rpartition('/')[0] for row in raw_sentence],
#                 "pos_tags": [row[POS_COL] for row in raw_sentence],
#                 "verb_stems": [row[VERB_STEM_COL] for row in raw_sentence],
#                 "ner_types": [row[NER_TYPE_COL] for row in raw_sentence],
#                 "zero_anaphora_indices": [row[ZERO_ANAPHORA_INDEX_COL] for row in raw_sentence],
#                 "coref_info": [row[COREF_COL] for row in raw_sentence],
#             }
#             clean_sentences.append(clean_sentence)
        
#         doc = {
#             "doc_id": doc_id,
#             "sentences": clean_sentences,
#             "coref_chains": chains,
#         }
#         docs.append(doc)

#     return docs


# dataset = DatasetDict({
#     "train": Dataset.from_list(read_formatted_docs_as_list(TRAIN_FNAME)),
#     "validation": Dataset.from_list(read_formatted_docs_as_list(VALIDATION_FNAME)),
#     "test": Dataset.from_list(read_formatted_docs_as_list(TEST_FNAME)),
# })

# dataset.push_to_hub("coref-data/korean_ecmt", private=True)
