"""
Convert korean_ecmt to indiscrim format
"""

import datasets
from kiwipiepy import Kiwi

from .utils.detokenize import detokenize_sentences


kiwi = Kiwi()


def detokenize(tokens):
    # e.g. kiwi.join([('길', 'NNG'), ('을', 'JKO'), ('묻', 'VV'), ('어요', 'EF')])
    token_tuples = [(tok["lemma"], tok["xpos"]) for tok in tokens]
    return kiwi.join(token_tuples)


def format_sentence(sent_and_index):
    """format a raw sentence in standardized indiscrim format"""
    index, raw_sentence = sent_and_index
    lemmas = raw_sentence["lemmas"]
    pos_tags = raw_sentence["pos_tags"]

    tokens = [{"id": i + 1, "text": w, "lemma": w, "xpos": pos_tags[i]} for i, w in enumerate(lemmas)]
    
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

    return {
        "id": example["doc_id"],
        "text": detokenize_sentences(sentences),
        "sentences": sentences,
        "coref_chains": coref_chains,
        "genre": "korean_wiki",
        "meta_data": {
            "comment": "detokenizer=kiwi",
        },
    }


def convert_korean_ecmt():
    dataset = datasets.load_dataset("coref-data/korean_ecmt_raw")

    # convert
    dataset = dataset.map(
        convert_to_indiscrim,
        remove_columns=dataset["train"].column_names,
        load_from_cache_file=False,
    )

    dataset.push_to_hub("coref-data/korean_ecmt_indiscrim")

