"""
Write the raw korean_ecmt dataset to the HuggingFace Hub.

The original text should be recoverable from the dataset at https://github.com/machinereading/crowdsourcing
"""

import os
import re

from datasets import Dataset, DatasetDict

from conll_coref_transform import conll_transform

# data files are available at this URL
DATA_URL = "https://github.com/machinereading/CR/blob/743f758e2b0c1fad6a06ce600b59ae882ab66c0e/input/"

TRAIN_FNAME = "nonJosa_train1345.NER5.v4_gold_conll"
VALIDATION_FNAME = "nonJosa_dev.NER5.v4_gold_conll"
TEST_FNAME = "whole.korean8_pd_NER.v4_gold_conll"

DOC_ID_PATTERN = r"#begin document \((.+)\); part \d+"

NER_dic = {'PERSON': 0, 'STUDY_FIELD' : 5, 'THEORY' : 5,
           'ARTIFACTS' : 5, 'ORGANIZATION' : 2, 'LOCATION' : 1,
           'CIVILIZATION' : 5, 'DATE' : 5, 'TIME': 4,
           'EVENT' : 3, 'ANIMAL' : 5, 'PLANT' : 5,
           'MATERIAL' : 5, 'TERM' : 5, 'JOB' : 5,
           'QUANTITY' : 5, 'ETC' : 5}

# These are all the columns that are used in the dataset
# Inferred from https://github.com/machinereading/CR/blob/743f758e2b0c1fad6a06ce600b59ae882ab66c0e/make_conll.py
TOK_IDX_COL = 2
LEMMA_COL = 3
POS_COL = 4
VERB_STEM_COL = 6
NER_TYPE_COL = 10
ZERO_ANAPHORA_INDEX_COL = 11
COREF_COL = 15


def read_raw_docs(fname):
    # map doc_id to list of sentences, each sentence is list of features
    docs = {}

    # parse all conll documents into a dict
    with open(fname, "r") as f:
        current_doc_id = None
        for line in f:
            line = line.rstrip()

            if line.startswith("#begin document"):
                assert current_doc_id is None
                full_doc_id = re.search(DOC_ID_PATTERN, line).group(1)
                current_doc_id = os.path.basename(full_doc_id)
                docs[current_doc_id] = []

            elif line.startswith("#end document"):
                assert current_doc_id is not None
                current_doc_id = None
                
            elif line:
                cols = line.split("\t")
                token_idx = int(cols[TOK_IDX_COL])
                if token_idx == 0:
                    docs[current_doc_id].append([])
                docs[current_doc_id][-1].append(cols)

    return docs


def read_formatted_docs_as_list(fname):
    raw_docs = read_raw_docs(fname)
    docs = []
    for doc_id, raw_sentences in raw_docs.items():
        # Return a list of chains,
        #     * each being a list of mentions,
        #     * each being a tuple of (sent, start, end), inclusive
        chains = conll_transform.compute_chains(raw_sentences)

        clean_sentences = []
        for raw_sentence in raw_sentences:
            clean_sentence = {
                "lemmas": [row[LEMMA_COL].rpartition('/')[0] for row in raw_sentence],
                "pos_tags": [row[POS_COL] for row in raw_sentence],
                "verb_stems": [row[VERB_STEM_COL] for row in raw_sentence],
                "ner_types": [row[NER_TYPE_COL] for row in raw_sentence],
                "zero_anaphora_indices": [row[ZERO_ANAPHORA_INDEX_COL] for row in raw_sentence],
                "coref_info": [row[COREF_COL] for row in raw_sentence],
            }
            clean_sentences.append(clean_sentence)
        
        doc = {
            "doc_id": doc_id,
            "sentences": clean_sentences,
            "coref_chains": chains,
        }
        docs.append(doc)

    return docs


dataset = DatasetDict({
    "train": Dataset.from_list(read_formatted_docs_as_list(TRAIN_FNAME)),
    "validation": Dataset.from_list(read_formatted_docs_as_list(VALIDATION_FNAME)),
    "test": Dataset.from_list(read_formatted_docs_as_list(TEST_FNAME)),
})

dataset.push_to_hub("coref-data/korean_ecmt", private=True)
