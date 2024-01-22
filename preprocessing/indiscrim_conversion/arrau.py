"""
Convert arrau to indiscrim format

Partly based on https://github.com/pitrack/incremental-coref/blob/main/conversion_scripts/convert_arrau.py
"""

import collections
import re
import datasets

from .utils.detokenize import detokenize, detokenize_sentences

coref_drop = 0
drop_counter = 0
min_drop = 0
total = 0

def word_id_to_global_index(word_id):
    return int(word_id.replace("word_", "")) - 1


def parse_span(span):
    if ".." in span:
        try:
            start, end = span.split("..")
        except:
            print(span)
            raise
    else:
        start = span
        end = span
    return word_id_to_global_index(start), word_id_to_global_index(end)


def convert_to_indiscrim(example, debug=False):
    global drop_counter
    global coref_drop
    global min_drop
    global total

    # get all markables from the dataset
    
    corpus = example["corpus"]
    document_name = example["document_name"]
    split = example["split"]
    
    word_markables = example["words"]
    lemma_markables = example["morph"]
    pos_markables = example["pos"]

    sentence_markables = example["sentence"]
    coref_markables = example["coref"]

    # generate maps for lemma and pos
    word_id_to_lemma = {x["span"]:x["lemma"] for x in lemma_markables}
    word_id_to_pos = {x["span"]:x["tag"] for x in pos_markables}

    # create sentences
    sentences = []
    global_to_local_index = {}
    global_index = 0
    for sent_i, raw_sentence in enumerate(sentence_markables):
        assert sent_i == int(raw_sentence["orderid"])
        if ".." in raw_sentence["span"]:
            start_word, end_word = raw_sentence["span"].split("..")
        else:
            start_word = raw_sentence["span"]
            end_word = raw_sentence["span"]
        start_index = word_id_to_global_index(start_word)
        end_index = word_id_to_global_index(end_word)

        raw_tokens = word_markables[start_index:end_index + 1]
        tokens = []
        for tok_i, raw_tok in enumerate(raw_tokens):
            tokens.append({
                "id": tok_i + 1,
                "text": raw_tok["text"],
                "lemma": word_id_to_lemma[raw_tok["id"]],
                "xpos": word_id_to_pos[raw_tok["id"]],
            })

            global_to_local_index[global_index] = (sent_i, tok_i)
            global_index += 1

        sentences.append({
            "id": sent_i + 1,
            "speaker": None,
            "text": detokenize(tokens),
            "tokens": tokens,
        })
        
    # create coref_chains
    # min_ids, sentenceid, span
        
    # entity id to mentions
    eid_to_spans = collections.defaultdict(list)
    for markable in coref_markables:

        total += 1

        if "coref_set" not in markable or not markable["coref_set"]:
            coref_drop += 1
            continue # no entity cluster given

        if "span" not in markable and "min_span" not in markable:
            continue # no spans

        # use min_span if possible otheriwse use span
        # min_span seems to be only given if span is split, and not in all such cases
        raw_span = markable["min_span"] if "min_span" in markable else markable["span"]

        # span is split
        if "," in raw_span:
            if debug:
                # print it to see what it looks like
                print(f"Skipping span {raw_span}")
                subspans = list(map(parse_span, raw_span.split(",")))
                for s, e in subspans:
                    print("Subspan:", " ".join([w["text"] for w in word_markables[s:e+1]]))
                s = subspans[0][0]
                e = subspans[-1][1]
                print("Full text:", " ".join([w["text"] for w in word_markables[s:e+1]]))
            
            # skip discontinuous spans
            min_drop += 1
            continue

        eid = markable["coref_set"]
        global_start, global_end = parse_span(raw_span)
        eid_to_spans[eid].append([global_start, global_end])

    coref_chains = []
    for eid, spans in eid_to_spans.items():
        chain = []
        for global_start, global_end in spans:
            sent_start, tok_start = global_to_local_index[global_start]
            sent_end, tok_end = global_to_local_index[global_end]

            if sent_start != sent_end:
                # skip mentions that cross sentence boundaries
                if debug:
                    print(corpus, example["document_name"])
                    print(eid)
                    print(f"{global_start} {global_end} {sent_start} {sent_end}")
                    print("Subspan:", " ".join([w["text"] for w in word_markables[global_start:global_end+1]]))
                drop_counter += 1
                continue
            chain.append([sent_start, tok_start, tok_end])

        if chain:
            coref_chains.append(chain)
    
    return {
        "id": example["document_name"],
        "text": detokenize_sentences(sentences),
        "sentences": sentences,
        "coref_chains": coref_chains,
        "genre": corpus,
        "split": example["split"], # keep split
        "meta_data": {"comment": "detokenizer=nltk"},
    }


def convert_arrau():
    dataset = datasets.load_dataset("coref-data/arrau_raw")
    dataset = dataset["train"]

    # convert
    dataset = dataset.map(
        convert_to_indiscrim,
        remove_columns=dataset.column_names,
        load_from_cache_file=False,
    )

    print(total, drop_counter, coref_drop, min_drop)

    # train/validation/test split
    training_sets = [dataset.filter(lambda x: x["split"] == "train", num_proc=16)]
    validation_sets = [dataset.filter(lambda x: x["split"] == "dev", num_proc=16)]
    test_sets = [dataset.filter(lambda x: x["split"] == "test", num_proc=16)]

    # for every genre not split, split as train/dev/test percent 80/10/10
    not_split = dataset.filter(lambda x: not x["split"], num_proc=16)
    genres = set(not_split["genre"])
    for genre in genres:
        not_split_genre = not_split.filter(lambda x: x["genre"] == genre, num_proc=16)

        genre_num_docs = len(not_split_genre["id"])
        print(f"Len of genre {genre}:", genre_num_docs)

        train_testvalid = not_split_genre.train_test_split(test_size=0.2 if genre_num_docs >= 10 else 2, seed=0)
        test_valid = train_testvalid["test"].train_test_split(test_size=0.5, seed=0)

        training_sets.append(train_testvalid["train"])
        validation_sets.append(test_valid["train"])
        test_sets.append(test_valid["test"])
        
    dataset = datasets.DatasetDict({
        "train": datasets.concatenate_datasets(training_sets),
        "validation": datasets.concatenate_datasets(validation_sets),
        "test": datasets.concatenate_datasets(test_sets),
    })

    dataset.remove_columns("split")
    
    dataset.push_to_hub("coref-data/arrau_indiscrim")
