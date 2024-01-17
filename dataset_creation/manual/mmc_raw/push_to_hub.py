"""
Write the raw mmc dataset to the HuggingFace Hub.
"""

from pathlib import Path
import pandas as pd
from datasets import Dataset, DatasetDict
import conll_transform

DATA_DIR = "data_creation/data/conll_format/"

def get_conll_file(path, split):
    """For a given path and split, return the conll data file"""
    return list(path.glob(f"{split}.*.v4_gold_conll"))[0]


def hotfix(sentences, fname, doc_name):
    # hotfixes
    if "mmc_fa_corrected/test.farsi.v4_gold_conll" in str(fname) and doc_name == "(s09e04c04t); part 004":
        assert sentences[0][8][-1] == "(3"
        sentences[0][8][-1] = "-"

    if "mmc_en/train.english.v4_gold_conll" in str(fname) and doc_name == "(s01e04c12t); part 012":
        assert sentences[8][6][-1] == "(0"
        sentences[8][2][-1] = "-"
        sentences[8][4][-1] = "-"
        sentences[8][6][-1] = "-"

    if "mmc_en/test.english.v4_gold_conll" in str(fname) and doc_name == "(s09e09c03t); part 003":
        assert sentences[14][0][-1] == "(13"
        sentences[14][0][-1] = "-"

    return sentences


def read_conll_file_as_hf_dataset(fname):
    docs = []
    for doc_name, sentences in conll_transform.read_file(fname).items():
        sentences = hotfix(sentences, fname, doc_name)

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

    return Dataset.from_list(docs)


config_paths = [f for f in Path(DATA_DIR).iterdir() if f.is_dir()]

for config_path in config_paths:
    config_name = config_path.stem

    data = {}
    for split in ["train", "dev", "test"]:
        fname = get_conll_file(config_path, split)
        data[split] = read_conll_file_as_hf_dataset(fname)

    dataset = DatasetDict(data)
    
    dataset.push_to_hub("coref-data/mmc_raw", config_name=config_name)
