"""
Convert knowref 60k
"""


import datasets

from ..utils.detokenize import detokenize
from ..utils.hash import hash_example


def option_to_mention(words, option):
    """given a single word option, find the corresponding mention of form [sent, start, end] inclusive"""
    index = words.index(option)
    return [0, index, index]


def convert_to_indiscrim(example):
    # get data fields
    swapped_sentence = example["swapped_sentence"]
    candidate_0 = example["candidate0"]
    candidate_1 = example["candidate1"]
    correct_candidate = example["correct_candidate"]
    annotation_strength = example["annotation_strength"]

    # manual fix
    if example["original_sentence"] == "Marc is short for Marcus but he 's only called Marc Guggenheim , not Marcus Guggenheim .":
        candidate_1 = "Gregoryus"

    # convert fields
    text = swapped_sentence
    options = [candidate_0, candidate_1]
    label = 0 if correct_candidate == "candidate_0" else 1
    words = text.split(" ") # already tokenized

    # find and reformat pronoun
    pronouns = [{"index": i, "text": w} for i, w in enumerate(words) if w[0] == '[' and w[-1] == ']']
    assert len(pronouns) == 1
    pronoun = pronouns[0]
    words[pronoun["index"]] = pronoun["text"][1:-1]

    # every example is one sentence
    sentences = []
    tokens = [{"id": i + 1, "text": w} for i, w in enumerate(words)]
    detokenized_text = detokenize(tokens)
    sentences.append({
        "id": 1,
        "speaker": None,
        "text": detokenized_text,
        "start_char": 0,
        "end_char": len(detokenized_text),
        "tokens": tokens,
    })

    # calculate coreference chains
        
    pronoun_mention = [0, pronoun["index"], pronoun["index"]] # [sent, start, end]
    # turn each mention into a cluster
    coref_chains = list(map(lambda x: [option_to_mention(words, x)], options))
    assert len(coref_chains) == len(options), f"Invalid number of options: {options} {coref_chains}"
    # add the pronoun to the correct cluster
    coref_chains[label].append(pronoun_mention)

    return {
        "id": hash_example([sentences, coref_chains]),
        "text": detokenized_text,
        "sentences": sentences,
        "coref_chains": coref_chains,
        "genre": "reddit_with_names_swapped",
        "meta_data": {
            "annotation_strength": annotation_strength,
            "comment": "detokenizer=nltk",
        },
    }


def convert_knowref_60k():
    dataset = datasets.load_dataset("coref-data/knowref_60k_raw")

    # convert
    dataset = dataset.map(
        convert_to_indiscrim,
        remove_columns=dataset["test"].column_names,
        load_from_cache_file=False,
        # num_proc=10,
    )

    dataset.push_to_hub("coref-data/knowref_60k_indiscrim")
