"""
Write the conll2012 dataset with conllu dependency parses to the HuggingFace Hub.
"""

from pathlib import Path
import re

import conll_transform
from datasets import Dataset, DatasetDict

DATA_DIR = Path("conllu/")

DOC_ID_PATTERN = r"\((.+)\); part (\d+)"

split_to_fname = {"train": "train", "validation": "dev", "test": "test"}


def read_conllu_file(fname):
    docs = []
    for doc_name, sentences in conll_transform.read_file(fname).items():
        try:
            coref_chains = conll_transform.compute_chains(sentences)
        except:
            print(f"{doc_name} compute chains failed at file {fname}")
            raise
        match = re.search(DOC_ID_PATTERN, doc_name)
        doc_id = match.group(1)
        part_name = int(match.group(2))
        docs.append({
            "doc_name": f"{doc_id}/part_{part_name}",
            "sentences": sentences,
            "coref_chains": coref_chains,
        })
    return docs


# Read data from conll files as one config

dataset_dict = {}
for split, fname_stem in split_to_fname.items():
    docs = read_conllu_file(DATA_DIR / f"{fname_stem}.conll")
    
    dataset_dict[split] = Dataset.from_list(docs)

    dataset = DatasetDict(dataset_dict)

dataset.push_to_hub("coref-data/conll2012_conllu", private=True)
