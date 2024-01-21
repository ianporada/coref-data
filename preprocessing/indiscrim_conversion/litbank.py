"""
Convert all conll 2012 configs to indiscrim format
"""

import datasets

from .utils.detokenize import detokenize


def format_sentence(sent_and_index):
    """format a raw sentence in standardized indiscrim format"""
    index, raw_sentence = sent_and_index
    tokens = [{"id": i, "text": w} for i, w in enumerate(raw_sentence)]
    
    return {
        "id": index,
        "speaker": None,
        "text": detokenize(tokens),
        "tokens": tokens,
    }


def convert_to_indiscrim(example):
    raw_sentences = example["sentences"]
    sentences = map(format_sentence, enumerate(raw_sentences))
    sentences = list(sentences)

    meta_data = {"comment": "sentence_detokenizer=nltk|doc_detokenizer=original_source"}
    meta_data = meta_data | example["meta_info"]

    return {
        "id": example["doc_name"],
        "text": example["original_text"],
        "sentences": sentences,
        "coref_chains": example["coref_chains"],
        "genre": "novel",
        "meta_data": meta_data,
    }


def convert_litbank_config(repo_name, config_name):
    dataset = datasets.load_dataset(repo_name, config_name)

    dataset = dataset.map(
        convert_to_indiscrim,
        remove_columns=["doc_name", "meta_info", "entities", "events", "original_text", "quotes"],
        load_from_cache_file=False,
        num_proc=8,
    )

    dataset.push_to_hub("coref-data/litbank_indiscrim", config_name)

def convert_litbank():
    # convert each config
    repo_name = "coref-data/litbank_raw"

    configs = datasets.get_dataset_config_names(repo_name)
    for config_name in configs:
        convert_litbank_config(repo_name, config_name)