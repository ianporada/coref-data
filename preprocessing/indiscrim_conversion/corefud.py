"""
Convert corefud to indiscrim format
"""

import re
import datasets

from .utils.detokenize import detokenize, detokenize_sentences


def parse_span(span):
    if "-" in span:
        start, end = span.split("-")
    else:
        start = span
        end = span
    return float(start), float(end)


def span_to_indices(span, tokens):
    """given span as (start, end) ords convert to indices"""
    start, end = span
    start_idx = -1
    end_idx = -1
    
    # what is the minimum syntactic head of this subspan
    # we will eventually keep only the subspan with the minimum head
    min_head = len(tokens)

    for i, tok in enumerate(tokens):
        if start == tok["id"]:
            start_idx = i

        if start_idx >= 0: # we are in the middle of the subspan
            head = tok["head"]
            if head: # zeros don't have a head
                min_head = min(min_head, tok["head"])

        if end == tok["id"]:
            end_idx = i
            break
    
    assert start_idx >= 0 and start_idx <= end_idx and end_idx < len(tokens), \
           f"Span {span} found invalid indices {start_idx} / {end_idx} for tokens {tokens}"

    return {"start_idx": start_idx, "end_idx": end_idx, "min_head": min_head}


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
            "id": sent_i + 1,
            "speaker": raw_sentence["speaker"],
            "text": raw_sentence["text"],
            "tokens": tokens,
        })

    # iterate through each entity and find the id of the start and end
    # ignore the meta information

    coref_chains = []
    for entity in example["coref_entities"]:

        chain = []
        for mention in entity: # find indices of token ids that match span
            
            # we include every annotation of coreference
            # however, we could not included discourse deixis ("link:disc") or briding anaphora

            sent_idx = sent_to_idx[mention["sent_id"]]
            toks = sentences[sent_idx]["tokens"]

            # get all (start, end) subspans
            subspans = map(parse_span, mention["span"].split(","))
            
            try:
                subspan_indices = map(lambda x: span_to_indices(x, toks), subspans)
            except:
                print(f"Sentence {mention["sent_id"]} failed in doc {example["doc_id"]}")
                raise

            # for discontinuous spans, represent them as the contiguous subspan with the minimum syntactic head
            subspan_with_min_head = min(subspan_indices, key=lambda x: x["min_head"])
            
            chain.append([sent_idx, subspan_with_min_head["start_idx"], subspan_with_min_head["end_idx"]])

        if chain:
            coref_chains.append(chain)
    
    return {
        "id": example["doc_id"],
        "text": detokenize_sentences(sentences),
        "sentences": sentences,
        "coref_chains": coref_chains,
        "genre": None,
        "meta_data": {"comment": "doc_detokenizer=nltk|sentence_detokenizer=original_source"},
    }


def convert_corefud_config(repo_name, config_name):
    dataset = datasets.load_dataset(repo_name, config_name)

    dataset = dataset.map(
        convert_to_indiscrim,
        remove_columns=dataset["train"].column_names,
        load_from_cache_file=False,
        # num_proc=8,
    )

    dataset.push_to_hub("coref-data/corefud_indiscrim", config_name)


def convert_corefud():
    # convert each config
    repo_name = "coref-data/corefud_raw"

    configs = datasets.get_dataset_config_names(repo_name)
    for config_name in configs:
        convert_corefud_config(repo_name, config_name)