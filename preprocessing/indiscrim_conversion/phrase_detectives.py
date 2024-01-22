"""
Convert phrase detectives to indiscrim format
"""

import re
import datasets

from .utils.detokenize import detokenize, detokenize_sentences


def format_sentence(sent_and_index):
    """format a raw sentence in standardized indiscrim format"""
    index, raw_sentence = sent_and_index
    tokens = [{"id": i + 1, "text": w[2]} for i, w in enumerate(raw_sentence)]
    
    return {
        "id": index + 1,
        "speaker": None,
        "text": detokenize(tokens),
        "tokens": tokens,
    }


def convert_to_indiscrim(example):
    raw_sentences = example["sentences"]
    sentences = map(format_sentence, enumerate(raw_sentences))
    sentences = list(sentences)

    coref_chains = example["coref_chains"]

    match = re.search(r"^\((.+)/(.+)\);", example["doc_name"])
    genre = match.group(1)
    id = match.group(2)

    return {
        "id": id,
        "text": detokenize_sentences(sentences),
        "sentences": sentences,
        "coref_chains": coref_chains,
        "genre": genre,
        "meta_data": {
            "comment": "detokenizer=nltk",
        },
    }


def convert_phrase_detectives():
    dataset = datasets.load_dataset("coref-data/phrase_detectives_raw", "conll_singletons")

    # convert
    dataset = dataset.map(
        convert_to_indiscrim,
        remove_columns=dataset["train"].column_names,
        load_from_cache_file=False,
    )

    # train/test split
    train_validation = dataset["train"].train_test_split(test_size=45, seed=0)
    dataset = datasets.DatasetDict({
        "train": train_validation["train"],
        "validation": train_validation["test"],
        "test": dataset["validation"],
    })

    dataset.push_to_hub("coref-data/phrase_detectives_indiscrim")

