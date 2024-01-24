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

import hashlib
import json
import re

import datasets
import stanza


nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma,depparse')


def hash_example(ex):
    return hashlib.md5(json.dumps(ex, sort_keys=True).encode("utf-8")).hexdigest()


def find_pronoun(sentences, pronoun, pronoun_loc):
    for sent_i, sent in enumerate(sentences):
        for tok_i, tok in enumerate(sent["tokens"]):
            print(tok)
            if tok["start_char"] == pronoun_loc:
                assert tok["text"] == pronoun
                return (sent_i, tok_i, tok_i)
    raise ValueError("Cannot find pronoun")


def find_option(sentences, text, option):
    option_start = text.index(option)
    option_end = option_start + len(option)

    start_token = None
    for sent_i, sent in enumerate(sentences):
        for tok_i, tok in enumerate(sent["tokens"]):
            if tok["start_char"] == option_start:
                start_token = (sent_i, tok_i)
            if start_token and tok["end_char"] == option_end:
                assert sent_i == start_token[0]
                return (sent_i, start_token[0], tok_i)
    raise ValueError("Cannot find option")


def convert_to_indiscrim(example):
    text = example["text"]
    pronoun = example["pronoun"]
    pronoun_loc = example["pronoun_loc"]
    quote = example["quote"]
    quote_loc = example["quote_loc"]
    options = example["options"]
    label = example["label"]
    source = example["source"]

    raw_sentences = nlp(text).to_dict()

    sentences = []
    for sent_i, tokens in enumerate(raw_sentences):
        non_mtw_tokens = 
        start_char = tokens[0]["start_char"]
        end_char = tokens[-1]["end_char"]
        sentences.append({
            "id": sent_i + 1,
            "speaker": None,
            "text": text[start_char:end_char],
            "start_char": start_char,
            "end_char": end_char,
            "tokens": tokens,
        })

    # calculate coreference chains
        
    pronoun_mention = find_pronoun(sentences, pronoun, pronoun_loc)
    # turn each mention into a cluster
    option_mentions = list(map(lambda x: [find_option(sentences, text, x)], options))
    # add the pronoun to the correct cluster
    option_mentions[label].append(pronoun_mention)
    coref_chains = option_mentions

    return {
        "id": hash_example(example),
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
