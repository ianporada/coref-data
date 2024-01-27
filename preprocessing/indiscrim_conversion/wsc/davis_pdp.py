"""
Convert pdp to indiscrim format

We could parse in batches as follows:
```
docs = [Document([], text=ex["text"]) for ex in examples]

parses = []
for i in tqdm(range(0, len(docs), batch_size)):
    batch_docs = docs[i:i+batch_size]
    parses += nlp(batch_docs)
```
which can also be done with
```
nlp.bulk_process(in_docs)
```
"""

import re

import datasets

from ..utils.hash import hash_example
from ..utils.parse import parse


def find_pronoun(sentences, pronoun, pronoun_loc):
    for sent_i, sent in enumerate(sentences):
        for tok_i, tok in enumerate(sent["tokens"]):
            if tok["start_char"] == pronoun_loc:
                assert tok["text"] == pronoun
                return [sent_i, tok_i, tok_i]
    raise ValueError("Cannot find pronoun")


def find_start_end(sentences, start_char, end_char):
    # find mention corresponding to start and end char
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
                    assert sent_i == start_token["sent_i"]
                    return [sent_i, start_token["tok_i"], tok_i]
    raise ValueError(f"Cannot find option at ({start_char}, {end_char}) within {sentences}")


def find_option(sentences, text, option):
    mentions = []
    option_starts = [m.start() for m in re.finditer(option, text)]
    for option_start in option_starts:
        option_end = option_start + len(option)
        mentions.append(find_start_end(sentences, option_start, option_end))
    return mentions


def convert_to_indiscrim(example):
    text = example["text"]
    pronoun = example["pronoun"]
    pronoun_loc = example["pronoun_loc"]
    quote = example["quote"]
    quote_loc = example["quote_loc"]
    options = example["options"]
    label = example["label"]
    source = example["source"]

    raw_sentences = parse(text)

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
        
    pronoun_mention = find_pronoun(sentences, pronoun, pronoun_loc)
    # turn each mention into a cluster
    coref_chains = list(map(lambda x: find_option(sentences, text, x), options))
    assert len(coref_chains) == len(options), f"Invalid number of options: {options} {coref_chains}"
    # add the pronoun to the correct cluster
    coref_chains[label].append(pronoun_mention)

    return {
        "id": hash_example([sentences, coref_chains]),
        "text": text,
        "sentences": sentences,
        "coref_chains": coref_chains,
        "genre": "novel",
        "meta_data": {
            "source": source,
            "comment": "detokenizer=source",
        },
    }


def convert_davis_pdp():
    dataset = datasets.load_dataset("coref-data/davis_pdp_raw")

    # convert
    dataset = dataset.map(
        convert_to_indiscrim,
        remove_columns=dataset["test"].column_names,
        load_from_cache_file=False,
    )

    dataset.push_to_hub("coref-data/davis_pdp_indiscrim")
