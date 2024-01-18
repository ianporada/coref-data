"""
Write the raw phrase detectives 3 dataset to the HuggingFace Hub.
"""

import xml.etree.ElementTree as ET
from pathlib import Path

import conll_transform
from datasets import Dataset, DatasetDict

DATA_DIR = Path("PD3.0_Train_dev/")

split_to_dir = {"train": "silver", "validation": "gold"}


def remove_nonreferring(sentences, keep_singletons):
    for s in sentences:
        for row in s:
            # make sure there is always a pipe between bounds and split
            coref_bounds = row[-1].replace(")(", ")|(").split("|")
            if keep_singletons: # prepend with integer to keep cluster_id unique
                coref_bounds = map(lambda x: x.replace("N", "1").replace("R", "2"),
                                   coref_bounds)
            else: # remove bounds with N (non-referring)
                coref_bounds = filter(lambda x: 'N' not in x, coref_bounds)
            coref_bounds = map(lambda x: x.replace("R", ""), coref_bounds)
            row[-1] = "|".join(coref_bounds) if coref_bounds else "-"
    return sentences


def read_conll_file(fname, keep_singletons):
    docs = []
    for doc_name, sentences in conll_transform.read_file(fname).items():
        sentences = remove_nonreferring(sentences, keep_singletons)
        try:
            coref_chains = conll_transform.compute_chains(sentences)
        except:
            print(f"{doc_name} compute chains failed at file {fname}")
            raise
        docs.append({
            "doc_name": doc_name,
            "sentences": sentences,
            "coref_chains": coref_chains,
        })
    return docs


# Read data from conll files as one config

for keep_singletons in [True, False]:
    dataset_dict = {}
    for split in split_to_dir.keys():
        split_dir = DATA_DIR / split_to_dir[split]
        
        docs = []
        for corpus_dir in split_dir.iterdir():
            corpus_name = corpus_dir.stem

            corpus_docs = []
            for document_path in corpus_dir.glob("CONLL/*.CONLL"):
                corpus_docs += read_conll_file(document_path, keep_singletons)

            for doc in corpus_docs:
                doc["corpus"] = corpus_name

            docs += corpus_docs
        
        dataset_dict[split] = Dataset.from_list(docs)

    dataset = DatasetDict(dataset_dict)
    config_name = "conll_singletons" if keep_singletons else "conll"
    dataset.push_to_hub("coref-data/phrase_detectives_raw", config_name)


def read_masxml_file(fname):
    return [{
        "document_name": fname.stem.replace("-game", ""),
        "xml": ET.tostring(ET.parse(fname).getroot()),
    }]


# Read raw data as a second config

dataset_dict = {}
for split in split_to_dir.keys():
    split_dir = DATA_DIR / split_to_dir[split]
    
    docs = []
    for corpus_dir in split_dir.iterdir():
        corpus_name = corpus_dir.stem

        corpus_docs = []
        for document_path in corpus_dir.glob("masxml/*-game.xml"):
            corpus_docs += read_masxml_file(document_path)

        for doc in corpus_docs:
            doc["corpus"] = corpus_name

        docs += corpus_docs
    
    dataset_dict[split] = Dataset.from_list(docs)

dataset = DatasetDict(dataset_dict)
dataset.push_to_hub("coref-data/phrase_detectives_raw", "masxml")
