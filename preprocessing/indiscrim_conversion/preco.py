"""
Convert preco to indiscrim format
"""

import datasets

from .utils.detokenize import detokenize, detokenize_sentences


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


def format_mention(mention):
    """adjust to inclusive bounds"""
    sent_id, start, end = mention
    return [sent_id, start, end - 1]


def convert_to_indiscrim(example):
    raw_sentences = example["sentences"]
    sentences = map(format_sentence, enumerate(raw_sentences))
    sentences = list(sentences)

    coref_chains = [list(map(format_mention, mentions)) for mentions in example["mention_clusters"]]

    return {
        "id": example["id"],
        "text": detokenize_sentences(sentences),
        "sentences": sentences,
        "coref_chains": coref_chains,
        "genre": "reading_comprehension_examination",
        "meta_data": {
            "comment": "detokenizer=nltk",
        },
    }


def convert_preco():
    dataset = datasets.load_dataset("coref-data/preco_raw")

    dataset = dataset.map(
        convert_to_indiscrim,
        remove_columns=["mention_clusters"],
        load_from_cache_file=False,
        num_proc=8,
    )

    # follow train/dev/test split of https://aclanthology.org/2021.crac-1.12/ by using last 500 train as dev
    dataset["test"] = dataset["validation"]

    num_train_docs = len(dataset["train"])
    dataset["validation"] = dataset["train"].filter(lambda ex:
                                                    int(ex["id"].replace("train_", "")) > num_train_docs - 500)
    dataset["train"] = dataset["train"].filter(lambda ex:
                                                    int(ex["id"].replace("train_", "")) <= num_train_docs - 500)

    dataset.push_to_hub("coref-data/preco_indiscrim")

