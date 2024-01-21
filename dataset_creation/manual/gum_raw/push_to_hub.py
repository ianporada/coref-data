"""
Write the raw gum dataset to the HuggingFace Hub.

Uploads universal dependencies, universal coreference, and OntoNotes style coreference chains.

Uses the published splits. Bridging anaphora is not yet fully parsed
"""

import copy
import glob
import os
import re

import conll_transform
from datasets import Dataset, DatasetDict
from stanza.utils.conll import FIELD_TO_IDX, CoNLL
from udapi.block.read.conllu import Conllu as ConlluReader

GUM_CONLLU_DIR = "gum/dep/"
GUM_CONLL_DIR = "gum/coref/gum/conll/"

ONTOGUM_CONLLU_DIR = "gum/coref/ontogum/conllu/"
ONTOGUM_CONLL_DIR = "gum/coref/ontogum/conll/"

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

    # hotfix unclosed span and missing token
    basename = os.path.basename(fname)
    if basename == "GUM_voyage_guadeloupe.conll":
        lines[1][-1] = "(1)"
    elif basename == "GUM_news_iodine.conll":
        lines[379][1] = "|"

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

            assert row[CONLLU_TEXT_COL] == token, \
                f"Mismatch {row[CONLLU_TEXT_COL]} and {token} at global index: {global_token_idx}"
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

        # for the first node in the tree, create a new sentence
        if not sentences or node.root.sent_id != sentences[-1]["sent_id"]:
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
            'ord': node.ord,
            'form': node.form,
            'lemma': node.lemma,
            'upos': node.upos,
            'xpos': node.xpos,
            'feats': str(node.feats),
            'head': node.parent.ord if node.parent else None,
            'deprel': node.deprel,
            'misc': str(node.misc),
            'coref_mentions': coref_mentions,
        }
        sentences[-1]['tokens'].append(token)

    coref_entities = []
    for entity in doc.coref_entities:
        coref_mentions = []
        for mention in entity.mentions:
            coref_mentions.append({
                "sent_id": mention.head.root.sent_id,
                'span': mention.span,
                'other': str(mention.other),
                'eid': mention.entity.eid,
                'eid_or_grp': mention.entity.eid_or_grp,
                'etype': mention.entity.etype,
            })
        coref_entities.append(coref_mentions)

    return sentences, coref_entities


# Parse the docs one by one

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
    try:
        ontogum_doc_dict, ontogum_coref_chains = compute_ontogum_coref_chains(doc_dict, raw_ontogum_lines)
    except Exception as e:
        print(f"Error in doc: {doc_id}")
        raise e

    # use udapi to read the corefud annotations from the conllu files
    corefud_sentences, coref_entities = read_corefud_data(conllu_fname)

    # merge doc_dict with corefud_sentences
    merged_sentences = []
    for sent_idx, sent in enumerate(doc_dict):
        corefud_sent = corefud_sentences[sent_idx]

        offset = 0
        for token_idx, token_dict in enumerate(sent):
            conllu_token = token_dict["text"]

            # make sure tokens align between what was read by stanza and udapi
            corefud_row = corefud_sent["tokens"][token_idx + offset]
            while not isinstance(corefud_row["ord"], int):
                offset += 1
                corefud_row = corefud_sent["tokens"][token_idx + offset]
            corefud_token = corefud_row["form"]
            if conllu_token != corefud_token:
                print("Tokens do not match:" \
                      f"{conllu_token} and {corefud_token} in {doc_id} at ({sent_idx}, {token_idx})")
                 

        corefud_sent["conll_rows"] = sent
        merged_sentences.append(corefud_sent)

    doc = {
        "doc_id": doc_id,
        "sentences": merged_sentences,
        "coref_entities": coref_entities,
        "ontogum_sentences": ontogum_doc_dict,
        "ontogum_coref_chains": ontogum_coref_chains,
    }
    docs.append(doc)


dev_ids = parse_list_of_split_ids(RAW_DEV_IDS)
test_ids = parse_list_of_split_ids(RAW_TEST_IDS)

train_docs = [doc for doc in docs if doc["doc_id"] not in dev_ids + test_ids]
validation_docs = [doc for doc in docs if doc["doc_id"] in dev_ids]
test_docs = [doc for doc in docs if doc["doc_id"] in test_ids]

dataset = DatasetDict({
    "train": Dataset.from_list(train_docs),
    "validation": Dataset.from_list(validation_docs),
    "test": Dataset.from_list(test_docs),
})

dataset.push_to_hub("coref-data/gum_raw", private=True)
