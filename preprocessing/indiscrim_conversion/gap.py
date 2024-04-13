"""
Convert knowref 60k
"""


import datasets

from .utils.detokenize import detokenize
from .utils.parse import parse, parse_no_ssplit


def reformat_raw_sentences(raw_sentences, text):
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
    
    return sentences


def option_to_mention(sentences, option, option_offset):
    """given option find span"""
    option_end_tok = option_offset + len(option)
    for sent_i, sent in enumerate(sentences):
        if not sent["start_char"] <= option_offset and option_offset <= sent["end_char"]:
            continue
        start_tok = None
        for tok_i, tok in enumerate(sent["tokens"]):
            if option_offset == tok["start_char"]:
                start_tok = tok_i
            
            # return the span if it was found
            if start_tok is not None:
                if option_end_tok == tok["end_char"]:
                    end_tok = tok_i
                    return [sent_i, start_tok, end_tok]
                elif tok["end_char"] and tok["end_char"] > option_end_tok:
                    if tok["start_char"] == None and (tok["text"] == "'s" or tok["lemma"] == "'s"):
                        end_tok = tok_i
                        return [sent_i, start_tok, end_tok]
                    if tok["start_char"] == None and len(tok["text"]) <= 2: # "''" appears after
                        end_tok = tok_i - 1
                        return [sent_i, start_tok, end_tok]
                    # exception for Paola example
                    if tok_i == start_tok and tok["text"][-2:] == "''":
                        end_tok = tok_i
                        return [sent_i, start_tok, end_tok]
                    
                    print("Unusual annotation: ", option, tok)
                    end_tok = tok_i
                    return [sent_i, start_tok, end_tok]
                    
                    

    
    raise ValueError("Mention not found: %s at offset %s in sentences %s" % (option, option_offset, sentences))


def convert_to_indiscrim(example):
    # get data fields
    example_id = example["ID"]
    example_url = example["URL"]
    text = example["Text"]
    pronoun = example["Pronoun"]
    pronoun_offset = example["Pronoun-offset"]
    option_a = example["A"]
    option_a_offset = example["A-offset"]
    option_a_coreferring = example["A-coref"]
    option_b = example["B"]
    option_b_offset = example["B-offset"]
    option_b_coreferring = example["B-coref"]

    raw_sentences = parse(text)
    sentences = reformat_raw_sentences(raw_sentences, text)

    # if any option spans multiple sentences, merge the sentences together
    # e.g. pass presplit sentences as nlp_no_ssplit(["This is a sentence.", "This is also a sentence."])

    sentence_boundaries = [(s["start_char"], s["end_char"]) for s in sentences]
    sentences_to_merge = []
    for option, offset in [(pronoun, pronoun_offset),
                           (option_a, option_a_offset),
                           (option_b, option_b_offset)]:
        start = offset
        end = offset + len(option)
        for sent_i, boundaries in enumerate(sentence_boundaries):
            sent_start, sent_end = boundaries
            if start >= sent_start and start < sent_end and end >= sent_end:
                sentences_to_merge.append(sent_i + 1)
    if sentences_to_merge:
        new_sentence_boundaries = []
        for sent_i, boundaries in enumerate(sentence_boundaries):
            if sent_i in sentences_to_merge:
                sent_start, sent_end = boundaries
                last_boundaries = new_sentence_boundaries[-1]
                new_sentence_boundaries[-1] = (last_boundaries[0], sent_end)
            else:
                new_sentence_boundaries.append(boundaries)
        sentence_strings = [text[start:end] for start, end in new_sentence_boundaries]

        raw_sentences = parse_no_ssplit(sentence_strings)
        sentences = reformat_raw_sentences(raw_sentences, text)

        # convert offsets to the new indices, these have a gap of 3 chars between each string
        old_index_to_new_index = [0] * len(text)
        new_index = 0
        for sent_i, boundaries in enumerate(new_sentence_boundaries):
            old_sent_start, old_sent_end = boundaries
            for i in range(old_sent_start, old_sent_end):
                old_index_to_new_index[i] = new_index
                new_index += 1
            new_index += 2

        pronoun_offset = old_index_to_new_index[pronoun_offset]
        option_a_offset = old_index_to_new_index[option_a_offset]
        option_b_offset = old_index_to_new_index[option_b_offset]

    pronoun_mention = option_to_mention(sentences, pronoun, pronoun_offset)
    option_a_mention = option_to_mention(sentences, option_a, option_a_offset)
    option_b_mention = option_to_mention(sentences, option_b, option_b_offset)

    coref_chains = []
    pronoun_chain = [pronoun_mention]
    if option_a_coreferring:
        pronoun_chain.append(option_a_mention)
    else:
        coref_chains.append([option_a_mention])
    if option_b_coreferring:
        pronoun_chain.append(option_b_mention)
    else:
        coref_chains.append([option_b_mention])
    coref_chains.append(pronoun_chain)

    return {
        "id": example_id,
        "text": text,
        "sentences": sentences,
        "coref_chains": coref_chains,
        "genre": "wikipedia",
        "meta_data": {
            "source": example_url,
            "comment": "detokenizer=source",
        },
    }


def convert_gap():
    dataset = datasets.load_dataset("coref-data/gap_raw")

    # convert
    dataset = dataset.map(
        convert_to_indiscrim,
        remove_columns=dataset["test"].column_names,
        load_from_cache_file=False,
        num_proc=16,
    )

    dataset.push_to_hub("coref-data/gap_indiscrim")
