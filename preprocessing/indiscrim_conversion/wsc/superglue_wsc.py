"""
Convert superglue wsc to indiscrim format
"""

import datasets

from ..utils.parse import parse, parse_no_ssplit


def find_pronoun(sentences, pronoun):
    """return start_char of pronoun"""
    for sent in sentences:
        for tok in sent["tokens"]:
            if tok["text"] == pronoun:
                return tok["start_char"]
    raise ValueError(f"Cannot find pronoun {pronoun} in {sentences}")


def find_option(sentences, option, option_start):
    # find mention corresponding to start and end char
    start_char = option_start
    end_char = option_start + len(option)

    start_token = None
    for sent_i, sent in enumerate(sentences):
        if end_char <= sent["start_char"] or start_char >= sent["end_char"]:
            continue # skip sentences outside of the range
        for tok_i, tok in enumerate(sent["tokens"]):
            if tok["start_char"] == start_char:
                start_token = {"sent_i": sent_i, "tok_i": tok_i}
            if start_token and tok["end_char"]:
                # if end or greater than end and posessive
                if tok["end_char"] == end_char or (tok["end_char"] > end_char and tok["text"] in ["'s"]):
                    assert sent_i == start_token["sent_i"], f"Option {option} starts at {start_token["sent_i"]} but ends at {sent_i} in {sentences}"
                    return [sent_i, start_token["tok_i"], tok_i]
    raise ValueError(f"Cannot find option '{option}' at ({start_char}, {end_char}) within {sentences}")


def convert_to_indiscrim(example):
    idx = example["idx"]
    text = example["text"]
    span1_index = example["span1_index"]
    span2_index = example["span2_index"]
    span1_text = example["span1_text"]
    span2_text = example["span2_text"]
    label = example["label"]

    # manual fix
    if idx == 42 and "Some day they might want to use it , but" in text:
        span2_index = 31 # was previously 30, off by one

    span_index_to_char_index = {0: 0}
    curr_span_index = 0
    for i, c in enumerate(text):
        if c == ' ':
            curr_span_index += 1
            span_index_to_char_index[curr_span_index] = i + 1

    raw_sentences = parse(text)

    # manual fix, error in parsing
    if idx >= 65 and idx <= 67 and "Mrs. Wyman" in text:
        raw_sentences = parse_no_ssplit(text)

    sentences = []
    for sent_i, tokens in enumerate(raw_sentences):
        # add mwt_token start and end to corresponding word
        mwt_tokens = [t for t in tokens if isinstance(t["id"], tuple)]
        non_mwt_tokens = [t for t in tokens if not isinstance(t["id"], tuple)]
        for mwt in mwt_tokens:
            non_mwt_tokens[mwt["id"][0] - 1]["start_char"] = mwt["start_char"]
            non_mwt_tokens[mwt["id"][-1] - 1]["end_char"] = mwt["end_char"]

        # set start and end to None if it doesn't exist
        for tok in non_mwt_tokens:
            for key in ["start_char", "end_char"]:
                if not key in tok:
                    tok[key] = None

        start_char = tokens[0]["start_char"]
        end_char = tokens[-1]["end_char"]
        sentences.append({
            "id": sent_i + 1,
            "speaker": None,
            "text": text[start_char:end_char],
            "start_char": start_char,
            "end_char": end_char,
            "tokens": non_mwt_tokens,
        })

    # calculate coreference chains
        
    mention_1 = find_option(sentences, span1_text, span_index_to_char_index[span1_index])
    mention_2 = find_option(sentences, span2_text, span_index_to_char_index[span2_index])
    if label == 1:
        coref_chains = [[mention_1, mention_2]] # same cluster
    else:
        coref_chains = [[mention_1], [mention_2]] # different clusters

    return {
        "id": idx,
        "text": text,
        "sentences": sentences,
        "coref_chains": coref_chains,
        "genre": "generated_by_undergraduate_students",
        "meta_data": {
            "comment": "detokenizer=source",
        },
    }


def convert_superglue_wsc():
    dataset = datasets.load_dataset("coref-data/superglue_wsc_raw", "wsc.fixed")

    # convert
    dataset = dataset.map(
        convert_to_indiscrim,
        remove_columns=dataset["train"].column_names,
        load_from_cache_file=False,
    )

    dataset.push_to_hub("coref-data/superglue_wsc_indiscrim")
