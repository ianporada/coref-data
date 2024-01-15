"""
Write the arrau 2.1 dataset to the HuggingFace Hub.
"""

import csv
import glob
import os
import xml.etree.ElementTree as ET

from conll_coref_transform import conll_transform
from datasets import Dataset, DatasetDict

# To recover:
# 1. List of words "Basedata/{}_words.xml"
# 2. Sentence boundaries "markables/{}_sentence_level.xml"
# 3. Phrase features <- redundant with coref "markables/{}_phrase_level.xml"
# 4. Lemmas "markables/{}_morph_level.xml"
# 5. Mention features "markables/{}_markable_level.xml"
# 6. Enamex types "markables/{}_enamex_level.xml"
# 7. Noun phrases (chunks?) "markables/{}_chunk_level.xml"
# 8. Coref data "markables/{}_coref_level.xml"
# 9. utterances (possibly) "markables/{}_utterance_level.xml"
# 10. pos tags "markables/{}_pos_level.xml"
# 11. other (possibly) "markables/{}_parse_level.xml" "markables/{}_unit_level.xml"

DATASET_DIR = "arrau_v2_1/ARRAU2.1/"

CORPORA = [
    {
        "dir": "Gnome_Subset2",
    },
    {
        "dir": "Pear_Stories",
    },
    {
        "dir": "RST_DTreeBank",
        "splits": ["dev", "test", "train"],
    },
    {
        "dir": "Trains_91",
    },
    {
        "dir": "Trains_93",
        "no_raw_files": True,
    },
]

def get_document_names(dataset):


for corpus in CORPORA:
    words = pass
    pos_tags = pass
    lemmas = pass

    tokens = pass


    sentence_boundaries = pass

    sentences = [tokens[start:end] for start, end in sentence_boundaries]

    markable_features = 

    raw_text = pass

    


    
# dataset = DatasetDict({
#     "train": Dataset.from_list([doc_name_to_doc[x] for x in train_docs]),
#     "validation": Dataset.from_list([doc_name_to_doc[x] for x in dev_docs]),
#     "test": Dataset.from_list([doc_name_to_doc[x] for x in test_docs]),
# })

# dataset.push_to_hub("coref-data/litbank_raw", f"split_{crossval_split}", private=True)
