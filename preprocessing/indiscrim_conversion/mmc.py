"""
Convert mmc to indiscrim format
"""

import re
import datasets

from .utils.detokenize import detokenize, detokenize_sentences


def format_sentence(sent_and_index):
    """format a raw sentence in standardized indiscrim format"""
    index, raw_sentence = sent_and_index

    # correct misparses
    for i, w in enumerate(raw_sentence):
        line = w[3:-4]
        if all([x == "na" for x in line[:5]]) and not line[5] == "na": # missing word token
            line = ["_"] + line
        line = line[:1] + [" ".join(line[6:])]
        raw_sentence[i] = line

    tokens = [{"id": i + 1, "text": w[0]} for i, w in enumerate(raw_sentence)]

    speaker = raw_sentence[0][1]
    assert all([w[1] == speaker for w in raw_sentence]), \
        f"All tokens in a sentence should have the same speaker: {speaker} {raw_sentence} {[w[1] == speaker for w in raw_sentence]}"
    
    return {
        "id": index + 1,
        "speaker": speaker,
        "text": detokenize(tokens),
        "tokens": tokens,
    }


def convert_to_indiscrim(example):
    raw_sentences = example["sentences"]
    sentences = map(format_sentence, enumerate(raw_sentences))
    sentences = list(sentences)

    coref_chains = example["coref_chains"]

    match = re.search(r"^\((.+)\); part (\d+)", example["doc_name"])
    clip_name = match.group(1)
    part = match.group(2)

    also_part = re.search(r"c([\d]{2})[tf]", clip_name).group(1)
    assert int(part) == int(also_part)

    genre = "tv_friends" if clip_name[-1] == "f" else "tv_the_big_bang_theory"

    return {
        "id": clip_name,
        "text": detokenize_sentences(sentences),
        "sentences": sentences,
        "coref_chains": coref_chains,
        "genre": genre,
        "meta_data": {
            "comment": "detokenizer=nltk",
        },
    }


def convert_mmc_config(repo_name, config_name):
    dataset = datasets.load_dataset(repo_name, config_name)

    # convert
    dataset = dataset.map(
        convert_to_indiscrim,
        remove_columns=dataset["train"].column_names,
        load_from_cache_file=False,
    )

    # train/test split
    dataset = datasets.DatasetDict({
        "train": dataset["train"],
        "validation": dataset["dev"],
        "test": dataset["test"],
    })

    dataset.push_to_hub("coref-data/mmc_indiscrim", config_name)


def convert_mmc():
    # convert each config
    repo_name = "coref-data/mmc_raw"

    configs = datasets.get_dataset_config_names(repo_name)
    for config_name in configs:
        convert_mmc_config(repo_name, config_name)
