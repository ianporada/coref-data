"""
Write the arrau 2.1 dataset to the HuggingFace Hub.

Some MMAX code modified from https://github.com/pitrack/incremental-coref/blob/main/conversion_scripts/convert_arrau.py
"""

import csv
import glob
import os
import xml.etree.ElementTree as ET

from conll_coref_transform import conll_transform
from datasets import Dataset, DatasetDict

# Not currently read but could be recovered:
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


def get_document_names(data_dir):
    return [f.replace(".header", "") for f in os.listdir(data_dir) if ".header" in f]

def word_id_to_index(word_id):
    return int(word_id.split("_")[1]) - 1

def span_to_ids(span):
  """Split span string into start and end ids"""
  if ".." in span:
    return span.split("..")
  return [span, span] # same start and end


def xml_words(data_dir, document_name):
    """Parse a list of words from xml file: [word, ...]"""
    fname = os.path.join(data_dir, "Basedata", document_name + "_words.xml")

    words = []
    for word in ET.parse(fname).getroot().iter():
        if not "id" in word.attrib:
            continue
        assert word_id_to_index(word.attrib["id"]) == len(words), "Words ids should be continuous"
        words.append(word.text)
    return words


def xml_sentence_spans(data_dir, document_name):
    """Parse sentence spans from xml file: [(word_start, word_end), ...]"""
    fname = os.path.join(data_dir, "markables", document_name + "_sentence_level.xml")

    sentence_spans = []
    for markable in ET.parse(fname).getroot().iter():
        if not "id" in markable.attrib:
            continue
        assert int(markable.attrib["orderid"]) == len(sentence_spans), "Sentence ids should be continuous"
        span = markable.attrib["span"]
        start, end = map(word_id_to_index, span_to_ids(span))
        sentence_spans.append((start, end))
    return sentence_spans


def xml_phrase_features(data_dir, document_name):
    """Parse phrase level features"""
    fname = os.path.join(data_dir, "markables", document_name + "_phrase_level.xml")

    phrase_features = {}
    for markable in ET.parse(fname).getroot().iter():
        if not "id" in markable.attrib:
            continue

        features = {
            "id": markable.attrib["id"],
            "span": map(word_id_to_index, span_to_ids(markable.attrib["span"])), # [start, end] word indices
            "raw_features": markable.attrib,
        }
        phrase_features[markable.attrib["id"]] = features
    return phrase_features


def xml_lemmas(data_dir, document_name):
    """Parse a list of lemmas from xml file"""
    fname = os.path.join(data_dir, "markables", document_name + "_morph_level.xml")

    lemmas = []
    for markable in ET.parse(fname).getroot().iter():
        if not "id" in markable.attrib:
            continue
        assert word_id_to_index(markable.attrib["span"]) == len(lemmas), "Words ids should be continuous"
        lemmas.append(markable.attrib["lemma"])
    return lemmas


def xml_pos_tags(data_dir, document_name):
    """Parse a list of pos tags from xml file"""
    fname = os.path.join(data_dir, "markables", document_name + "_pos_level.xml")

    pos_tags = []
    for markable in ET.parse(fname).getroot().iter():
        if not "id" in markable.attrib:
            continue
        assert word_id_to_index(markable.attrib["span"]) == len(pos_tags), "Words ids should be continuous"
        pos_tags.append(markable.attrib["tag"])
    return pos_tags


def xml_mention_features(data_dir, document_name):
    """Mention features"""
    fname = os.path.join(data_dir, "markables", document_name + "_markable_level.xml")

    features = {}
    for markable in ET.parse(fname).getroot().iter():
        if not "id" in markable.attrib:
            continue

        markable_features = {
            "sentenceid": int(markable.attrib["sentenceid"]),
            "span": map(word_id_to_index, span_to_ids(markable.attrib["span"])), # [start, end] word indices
            "min_span": map(word_id_to_index, span_to_ids(markable.attrib["min_ids"])), # [start, end] word indices
            "raw_features": markable.attrib,
        }
        features[markable.attrib["id"]] = markable_features
    return features


def xml_enamex_types(data_dir, document_name):
    """Enamex types"""
    fname = os.path.join(data_dir, "markables", document_name + "_enamex_level.xml")

    features = {}
    for markable in ET.parse(fname).getroot().iter():
        if not "id" in markable.attrib:
            continue

        markable_features = {
            "span": map(word_id_to_index, span_to_ids(markable.attrib["span"])), # [start, end] word indices
            "tag": markable.attrib["tag"]
        }
        features[markable.attrib["id"]] = markable_features
    return features


def xml_chunks(data_dir, document_name):
    """Read all np spans / chunks"""
    fname = os.path.join(data_dir, "markables", document_name + "_chunk_level.xml")

    features = {}
    for markable in ET.parse(fname).getroot().iter():
        if not "id" in markable.attrib:
            continue

        markable_features = {
            "span": map(word_id_to_index, span_to_ids(markable.attrib["span"])), # [start, end] word indices
            "tag": markable.attrib["tag"]
        }
        features[markable.attrib["id"]] = markable_features
    return features


def xml_utterances(data_dir, document_name):
    """Read all utterance spans"""
    fname = os.path.join(data_dir, "markables", document_name + "_utterance_level.xml")

    features = {}
    for markable in ET.parse(fname).getroot().iter():
        if not "id" in markable.attrib:
            continue

        markable_features = {
            "span": map(word_id_to_index, span_to_ids(markable.attrib["span"])), # [start, end] word indices
        }
        features[markable.attrib["id"]] = markable_features
    return features


def xml_coref(data_dir, document_name):
    """Parse coref data from an xml file"""
    fname = os.path.join(data_dir, "markables", document_name + "_coref_level.xml")

    features = {}
    for markable in ET.parse(fname).getroot().iter():
        if not "id" in markable.attrib:
            continue

        markable_features = {
            "sentenceid": int(markable.attrib["sentenceid"]),
            "span": map(word_id_to_index, span_to_ids(markable.attrib["span"])), # [start, end] word indices
            "min_span": map(word_id_to_index, span_to_ids(markable.attrib["min_ids"])), # [start, end] word indices
            "raw_features": markable.attrib,
        }
        features[markable.attrib["id"]] = markable_features
    return features








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
