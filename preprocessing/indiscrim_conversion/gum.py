"""
Convert gum and ontogum to indiscrim format
"""

import re
import datasets

from .utils.detokenize import detokenize, detokenize_sentences


def name_to_genre(doc_id):
    return re.search("GUM_(.*)_", doc_id).group(1)


def parse_span(span):
    if "-" in span:
        start, end = span.split("-")
    else:
        start = span
        end = span
    return int(start), int(end)


def format_ontogum_sentence(sent_and_index):
    """format a raw sentence in standardized indiscrim format"""
    index, raw_sentence = sent_and_index
    tokens = [{"id": i, "text": w} for i, w in enumerate(raw_sentence)]
    
    return {
        "id": index,
        "speaker": None,
        "text": detokenize(tokens),
        "tokens": tokens,
    }


def convert_to_ontogum_indiscrim(example):
    # merge necessary features from ontogum sentences and sentences
    sentences = []
    for i, ontogum_sentence in enumerate(example["ontogum_sentences"]):
        raw_sentence = example["sentences"][i]
        sentences.append({
            "id": i,
            "speaker": raw_sentence["speaker"],
            "text": raw_sentence["text"],
            "tokens": ontogum_sentence,
        })

    return {
        "id": example["doc_id"],
        "text": detokenize_sentences(sentences),
        "sentences": sentences,
        "coref_chains": example["ontogum_coref_chains"],
        "genre": name_to_genre(example["doc_id"]),
        "meta_data": {"comment": "doc_detokenizer=nltk|sentence_detokenizer=original_source"},
    }


def convert_to_indiscrim(example):
    # convert a regular example to default indicscrim instance
    sent_to_idx = {}

    raw_sentences = example["sentences"]
    sentences = []
    for sent_i, raw_sentence in enumerate(raw_sentences):
        sent_to_idx[raw_sentence["sent_id"]] = sent_i
        tokens = []
        for tok_i, raw_token in enumerate(raw_sentence["tokens"]):
            tokens.append({
                "id": raw_token["ord"],
                "text": raw_token["form"],
                "lemma": raw_token["lemma"],
                "upos": raw_token["upos"],
                "xpos": raw_token["xpos"],
                "head": raw_token["head"],
                "deprel": raw_token["deprel"],
                "feats": raw_token["feats"],
                "misc": raw_token["misc"],
            })

        sentences.append({
            "id": sent_i,
            "speaker": raw_sentence["speaker"],
            "text": raw_sentence["text"],
            "tokens": tokens,
        })

    # iterate through each entity and find the id of the start and end
    # ignore the meta information
    # gum does not have split atecedents

    coref_chains = []
    for entity in example["coref_entities"]:
        chain = []
        for mention in entity: # find indices of token ids that match span
            sent_idx = sent_to_idx[mention["sent_id"]]
            toks = sentences[sent_idx]["tokens"]
            start, end = parse_span(mention["span"])
            start_idx = -1
            end_idx = -1
            for i, tok in enumerate(toks):
                if start == tok["id"]:
                    start_idx = i
                if end == tok["id"]:
                    end_idx = i
                    break
            assert start_idx >= 0 and start_idx <= end_idx and end_idx < len(toks)
            chain.append([sent_idx, start_idx, end_idx])
        coref_chains.append(chain)
    
    return {
        "id": example["doc_id"],
        "text": detokenize_sentences(sentences),
        "sentences": sentences,
        "coref_chains": coref_chains,
        "genre": name_to_genre(example["doc_id"]),
        "meta_data": {"comment": "doc_detokenizer=nltk|sentence_detokenizer=original_source"},
    }


def convert_ontogum(dataset: datasets.DatasetDict):
    dataset = dataset.map(
        convert_to_ontogum_indiscrim,
        remove_columns=dataset["train"].column_names,
        load_from_cache_file=False,
        # num_proc=8,
    )

    dataset.push_to_hub("coref-data/gum_indiscrim", "ontogum")


def convert_original_gum(dataset: datasets.DatasetDict):
    dataset = dataset.map(
        convert_to_indiscrim,
        remove_columns=dataset["train"].column_names,
        load_from_cache_file=False,
        # num_proc=8,
    )

    dataset.push_to_hub("coref-data/gum_indiscrim", "original")


def convert_gum():
    # convert each config
    dataset = datasets.load_dataset("coref-data/gum_raw")

    convert_ontogum(dataset)
    
    convert_original_gum(dataset)