"""
Write the arrau 2.1 dataset to the HuggingFace Hub.

Some MMAX code modified from https://github.com/pitrack/incremental-coref/blob/main/conversion_scripts/convert_arrau.py

Does not read raw data since there is a mismatch in file names, although some of the original text documents
could be recovered from the original dataset.
"""

import glob
import os
import xml.etree.ElementTree as ET

from datasets import Dataset, DatasetDict

DATASETS_DIR = "arrau_v2_1/ARRAU2.1/"

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
    },
]


def get_document_names(data_dir):
    return [f.replace(".header", "") for f in os.listdir(data_dir) if ".header" in f]


def word_id_to_index(word_id):
    return int(word_id.split("_")[1]) - 1


def read_xml_mmax_file(fname):
    """Read an XML file in MMAX format."""
    return [m for m in ET.parse(fname).getroot().iter() if "id" in m.attrib]


def read_words_file(fname):
    markables = read_xml_mmax_file(fname)
    assert all([word_id_to_index(m.attrib["id"]) == i for i, m in enumerate(markables)]), \
           "Words ids should be continuous"
    return [{"id": m.attrib["id"], "text": m.text} for m in markables]


def read_features_file(fname):
    markables = read_xml_mmax_file(fname)
    return [m.attrib for m in markables]


def read_raw_file(fname):
    with open(fname) as f:
        return f.read()


def read_doc(data_dir, document_name):
    """Read all data pertaining to a given doc"""
    doc_dict = {"document_name": document_name}

    words_fname = os.path.join(data_dir, "Basedata", document_name + "_words.xml")
    doc_dict["words"] = read_words_file(words_fname)

    features_fnames = glob.glob(os.path.join(data_dir, "markables", document_name + "_*_level.xml"))
    for feature_file_name in features_fnames:
        feature_name = os.path.basename(feature_file_name)
        feature_name = feature_name.replace("_level.xml", "").replace(document_name + "_", "")
        doc_dict[feature_name] = read_features_file(feature_file_name)

    return doc_dict


def read_mmax_data(corpus_name, split=None):
    """Read all mmax data for a given corpus and split"""
    if split:
        data_dir = os.path.join(DATASETS_DIR, corpus_name, split, "MMAX")
    else: 
        data_dir = os.path.join(DATASETS_DIR, corpus_name, "MMAX")
    doc_names = get_document_names(data_dir)
    docs = [read_doc(data_dir, document_name) for document_name in doc_names]
    for doc in docs:
        doc["corpus"] = corpus_name
        doc["split"] = split
    return docs


# Upload to HuggingFace

all_docs = []
for corpus in CORPORA:
    corpus_name = corpus["dir"]
    splits = corpus["splits"] if "splits" in corpus else [None]

    for split in splits:
        all_docs += read_mmax_data(corpus_name, split)


dataset = Dataset.from_list(all_docs)
dataset.push_to_hub("coref-data/arrau_raw", private=True)
