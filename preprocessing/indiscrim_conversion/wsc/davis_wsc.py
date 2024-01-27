"""
Convert davis_wsc to indiscrim format
```
"""

import hashlib
import json
import re

import datasets

from ..utils.parse import parse


def hash_example(ex):
    return hashlib.md5(json.dumps(ex, sort_keys=True).encode("utf-8")).hexdigest()


def find_pronoun(sentences, pronoun, pronoun_loc):
    for sent_i, sent in enumerate(sentences):
        for tok_i, tok in enumerate(sent["tokens"]):
            if tok["start_char"] == pronoun_loc:
                assert tok["text"] == pronoun
                return [sent_i, tok_i, tok_i]
    raise ValueError("Cannot find pronoun")


def find_start_end(sentences, start_char, end_char, option=None):
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
    raise ValueError(f"Cannot find option at ({start_char}, {end_char}) '{option}' within {sentences}")


def find_all_option_starts(option, text):
    starts = [m.start() for m in re.finditer(option, text)]

    if option == "the key": # manual override
        return starts[:1]
    
    return starts


def get_fixed_option_starts(sentences, text, option):
    new_option = option
    option_starts = find_all_option_starts(new_option, text)

    if not option_starts: # try lowercase option
        new_option = option.lower()
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts: # try capitalization of first char of option
        new_option = option[:1].upper() + option[1:]
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "the suitcase": # match the brown suitcase to the suitcase
        new_option = "the brown suitcase"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The son": # manual alignment
        new_option = "his son"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "Tina's drawing": # TODO: annotate this as a null pronoun
        new_option = "Tina's"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The younger students": # manual alignment
        new_option = "the younger ones"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The oak tree": # manual alignment
        new_option = "an oak tree"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The gap": # manual alignment
        new_option = "a gap"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The hair": # manual alignment
        new_option = "hair"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The meeting": # manual alignment
        new_option = "My meeting"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The pillar": # manual alignment
        new_option = "a pillar"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The announcement": # manual alignment
        new_option = "an announcement"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The subway": # manual alignment
        new_option = "a subway"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The concert": # manual alignment
        new_option = "the outdoor concert"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The rag": # manual alignment
        new_option = "an old rag"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The map": # manual alignment
        new_option = "my map"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The building": # manual alignment
        new_option = "this building"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The spot under the tree": # manual alignment
        new_option = "a spot under the tree"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "Anne's daughter": # manual alignment
        new_option = "a daughter"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "Alice's daughter": # manual alignment
        new_option = "her daughter"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "the guy in uniform": # manual alignment
        new_option = "some guy in a military uniform" # TODO: interesting modifer: # with a huge read beard
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The chewing gum": # manual alignment
        new_option = "chewing gum"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The man": # manual alignment
        new_option = "a man"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The juggler": # manual alignment
        new_option = "a man"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The old house": # manual alignment
        new_option = "his house"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The new house": # manual alignment
        new_option = "a new one"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The flute": # manual alignment
        new_option = "her flute"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The piece": # manual alignment
        new_option = "one of her favorite pieces"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The chair": # manual alignment
        new_option = "a chair"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The backpack": # manual alignment
        new_option = "my backpack"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The article": # manual alignment
        new_option = "an article"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The sand castle": # manual alignment
        new_option = "a sand castle"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The flag": # manual alignment
        new_option = "a toy flag"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The cloud": # manual alignment
        new_option = "a thick cloud"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The shepherds": # manual alignment
        new_option = "shepherds"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The sheep": # manual alignment
        new_option = "sheep"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "Mary's daughter": # manual alignment
        new_option = "Anne" # TODO: her daughter Anne
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The tree": # manual alignment
        new_option = "that tree"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The axe": # manual alignment
        new_option = "that axe"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The TV": # manual alignment
        new_option = "TV"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "Kamchatka": # manual alignment TODO: fix
        new_option = "Kamtchatka"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The minnow": # manual alignment
        new_option = "a minnow"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The duck": # manual alignment
        new_option = "that duck"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The shark": # manual alignment
        new_option = "a shark"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "Prehistoric humans": # manual alignment
        new_option = "humans"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The fish": # manual alignment
        new_option = "three species of fish"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The crutches": # manual alignment
        new_option = "crutches"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The opponents": # manual alignment
        new_option = "opponents"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "copies of the newsletter": # manual alignment
        new_option = "copies of our newsletter"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The coffee": # manual alignment
        new_option = "my coffee"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "The boy": # manual alignment
        new_option = "the sleeping boy"
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option == "Pam and Paul": # manual alignment
        new_option = "Paul" # TODO: split antecedents
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option.startswith("The "):
        new_option = option.replace("The ", "his ")
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option.startswith("The "):
        new_option = option.replace("The ", "her ")
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option.startswith("The "):
        new_option = option.replace("The ", "my ")
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option.startswith("The "):
        new_option = option.replace("The ", "a ")
        option_starts = find_all_option_starts(new_option, text)

    if not option_starts and option.startswith("The "):
        new_option = option.replace("The ", "an ")
        option_starts = find_all_option_starts(new_option, text)

    if option == "The teller": # manual alignment
        new_option = "one of the tellers"
        option_starts = find_all_option_starts(new_option, text)

    return option_starts, new_option


def find_option(sentences, text, option): # manual exceptions based on the Toshniwal et al. CRAC paper
    mentions = []

    option_starts, new_option = get_fixed_option_starts(sentences, text, option)
    assert option_starts, f"Mention '{option}' not found: '{text}'"

    for option_start in option_starts:
        option_end = option_start + len(new_option)
        mentions.append(find_start_end(sentences, option_start, option_end, option))
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
        "genre": "expert_generated",
        "meta_data": {
            "source": source,
            "comment": "detokenizer=source",
        },
    }


def convert_davis_wsc_config(repo_name, config_name):
    dataset = datasets.load_dataset(repo_name, config_name)

    # convert
    dataset = dataset.map(
        convert_to_indiscrim,
        remove_columns=dataset["test"].column_names,
        load_from_cache_file=False,
    )

    dataset.push_to_hub("coref-data/davis_wsc_indiscrim", config_name)


def convert_davis_wsc():
    # convert each config
    repo_name = "coref-data/davis_wsc_raw"

    configs = datasets.get_dataset_config_names(repo_name)
    for config_name in configs:
        convert_davis_wsc_config(repo_name, config_name)
