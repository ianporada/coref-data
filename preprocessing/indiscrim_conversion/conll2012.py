"""
Convert all conll 2012 configs to indiscrim format
"""

import collections
from functools import partial
import re

import datasets

from .utils.detokenize import detokenize, detokenize_sentences

GENRE_CODE_TO_GENRE = {
    "nw": "newswire",
    "bc": "broadcast_conversation",
    "bn": "broadcast_news",
    "mz": "magazine",
    "nw": "newswire",
    "pt": "pivot",
    "tc": "telephone_conversation",
    "wb": "weblogs",
}

CHINESE_V4_POS_TAGS = ["X", "AD", "AS", "BA", "CC", "CD", "CS", "DEC", "DEG", "DER", "DEV", "DT", "ETC", "FW", "IJ", "INF", "JJ", "LB", "LC", "M", "MSP", "NN", "NR", "NT", "OD", "ON", "P", "PN", "PU", "SB", "SP", "URL", "VA", "VC", "VE", "VV",]
ENGLISH_V4_POS_TAGS = ["XX", "``", "$", "''", ",", "-LRB-", "-RRB-", ".", ":", "ADD", "AFX", "CC", "CD", "DT", "EX", "FW", "HYPH", "IN", "JJ", "JJR", "JJS", "LS", "MD", "NFP", "NN", "NNP", "NNPS", "NNS", "PDT", "POS", "PRP", "PRP$", "RB", "RBR", "RBS", "RP", "SYM", "TO", "UH", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "WDT", "WP", "WP$", "WRB",]
ENGLISH_V12_POS_TAGS = ["XX", "``", "$", "''", "*", ",", "-LRB-", "-RRB-", ".", ":", "ADD", "AFX", "CC", "CD", "DT", "EX", "FW", "HYPH", "IN", "JJ", "JJR", "JJS", "LS", "MD", "NFP", "NN", "NNP", "NNPS", "NNS", "PDT", "POS", "PRP", "PRP$", "RB", "RBR", "RBS", "RP", "SYM", "TO", "UH", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "VERB", "WDT", "WP", "WP$", "WRB",]

NAMED_ENTITY_TAGS = ["O", "B-PERSON", "I-PERSON", "B-NORP", "I-NORP", "B-FAC", "I-FAC", "B-ORG", "I-ORG", "B-GPE", "I-GPE", "B-LOC", "I-LOC", "B-PRODUCT", "I-PRODUCT", "B-DATE", "I-DATE", "B-TIME", "I-TIME", "B-PERCENT", "I-PERCENT", "B-MONEY", "I-MONEY", "B-QUANTITY", "I-QUANTITY", "B-ORDINAL", "I-ORDINAL", "B-CARDINAL", "I-CARDINAL", "B-EVENT", "I-EVENT", "B-WORK_OF_ART", "I-WORK_OF_ART", "B-LAW", "I-LAW", "B-LANGUAGE", "I-LANGUAGE",]


def split_doc_into_doc_parts(example):
    """take a doc and return the doc parts"""
    doc_parts_dict = {} # {0: [], 1:[], ...}
    for sent_dict in example['sentences'][0]:
        sent_part_id = sent_dict['part_id']
        if sent_part_id in doc_parts_dict:
            doc_parts_dict[sent_part_id].append(sent_dict)
        else:
            doc_parts_dict[sent_part_id] = [sent_dict]
    document_id = example['document_id'][0]
    return {'document_id': [f'{document_id}/part_{k}' for k in doc_parts_dict],
            'sentences': [doc_parts_dict[k] for k in doc_parts_dict]}


def clean_arabic_text(text):
    """
    From https://github.com/juntaoy/aracoref/blob/main/preprocess_arabic.py
    Modified by https://github.com/pitrack/incremental-coref/conversion_scripts/minimize.py
    """
    original = text
    # remove tashkeel
    text = text.replace('{', 'ا')
    text = text.replace('}', 'ا')

    #text = text.replace('-','')
    p_tashkeel = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
    text = re.sub(p_tashkeel, "", text)

    #Other typos in the conll files
    text = text.replace('ه`ذا', 'هذا')
    text = text.replace('ه`ذه', 'هذه')
    text = text.replace('ه`ذين', 'هذين')
    text = text.replace('الل`ه','الله')
    text = text.replace('ذ`لك', 'ذلك')
    text = text.replace('إل`ه','إله')

    # Additional for subtoken map reasons, rarely return original
    if len(text) == 0:
        return original
    return text


def normalize_word(word, config_name):
    if config_name == "arabic_v4":
        word = clean_arabic_text(word[:word.find("#")])
    if word == "/." or word == "/?":
        return word[1:]
    else:
        return word


def format_sentence(sent_and_index, config=None):
    """format a raw sentence in standardized indiscrim format"""
    index, raw_sentence = sent_and_index
    tokens = [{"id": i, "text": normalize_word(w, config)} for i, w in enumerate(raw_sentence["words"])]

    for i, xpos in enumerate(raw_sentence["pos_tags"]):
        if config == "english_v4":
            xpos_tag = ENGLISH_V4_POS_TAGS[xpos]
        elif config == "english_v12":
            xpos_tag = ENGLISH_V12_POS_TAGS[xpos]
        elif config == "chinese_v4":
            xpos_tag = CHINESE_V4_POS_TAGS[xpos]
        else:
            xpos_tag = xpos
        tokens[i]["xpos"] = xpos_tag
    
    return {
        "id": index,
        "speaker": raw_sentence["speaker"],
        "text": detokenize(tokens),
        "tokens": tokens,
    }




def convert_doc_into_indiscrim(example, config=None):
    """convert to standard indiscrim format"""
    id = example["document_id"][0]
    raw_sentences = example["sentences"][0]
    
    # format sentences
    format_sentence_partial = partial(format_sentence, config=config)
    sentences = map(format_sentence_partial, enumerate(raw_sentences))
    sentences = list(sentences)

    # compute coref chains
    cluster_id_to_mentions = collections.defaultdict(list)
    for sent_i, sentence in enumerate(raw_sentences):
        for coref_span in sentence["coref_spans"]:
            cluster_id, start_index, end_index = coref_span
            cluster_id_to_mentions[cluster_id].append([sent_i, start_index, end_index])
    coref_chains = list(cluster_id_to_mentions.values())

    genre_code = id[:2]
    genre = GENRE_CODE_TO_GENRE[genre_code]

    indiscrim_doc = {
        "id": id,
        "text": detokenize_sentences(sentences),
        "sentences": sentences,
        "coref_chains": coref_chains,
        "genre": genre,
        "meta_data": {
            "comment": "detokenizer=nltk",
        },
    }

    # convert to dataset format of key: list[values]
    return {k: [v] for k, v in indiscrim_doc.items()}


def add_conllu_columns(sentences, conllu_dict):
    for sent_i, sent in enumerate(sentences):
        for tok_i, tok in enumerate(sent["tokens"]):
            conllu_tok = conllu_dict[sent_i][tok_i]
            if conllu_tok["xpos"] != tok["xpos"]:
                print(f"xpos mismatch: {conllu_tok["xpos"]} and {tok["xpos"]}")
            conllu_tok.pop("text", None)
            conllu_tok.pop("xpos", None)
            tok = tok | conllu_tok
    return sentences


def word_line_to_dict(line):
    # the conllu data only has certain columns filled
    return {
        "text": line[1],
        "upos": line[3],
        "xpos": line[4],
        "head": 0 if line[7] == "root" else int(line[6]),
        "deprel": line[7],
    }


def sentences_to_conll_dict(sentences):
    return [[word_line_to_dict(word) for word in s] for s in sentences]


def add_conllu_parse_info(dataset):
    conllu_dataset = datasets.load_dataset("coref-data/conll2012_conllu")

    # convert conllu_dataset into dict mapping doc_name to sentences
    id_to_conll_dict = {}
    for split in ["train", "validation", "test"]:
        for ex in conllu_dataset[split].iter(1):
            id = ex["doc_name"][0]
            sentences = ex["sentences"][0]
            id_to_conll_dict[id] = sentences_to_conll_dict(sentences)
    
    dataset = dataset.map(lambda ex: {
            "sentences": add_conllu_columns(ex["sentences"], id_to_conll_dict[ex["id"]])
        },
        load_from_cache_file=False,
    )

    return dataset


def convert_conll2012_config(repo_name, config_name, num_proc=8):
    dataset = datasets.load_dataset(repo_name, config_name)

    # split each document into the annotated parts
    dataset = dataset.map(
        split_doc_into_doc_parts,
        batched=True,
        batch_size=1,
        num_proc=num_proc,
        load_from_cache_file=False,
    )

    # reformat
    convert_doc_into_indiscrim_partial = partial(convert_doc_into_indiscrim, config=config_name)
    dataset = dataset.map(
        convert_doc_into_indiscrim_partial,
        remove_columns=["document_id"], # remove old columns
        batched=True,
        batch_size=1,
        load_from_cache_file=False,
        # num_proc=num_proc,
    )

    # get conllu parse information for english_v4
    if config_name == "english_v4":
        dataset = add_conllu_parse_info(dataset)

    dataset.push_to_hub("coref-data/conll2012_indiscrim", config_name)


def convert_conll2012():
    # convert each config
    repo_name = "coref-data/conll2012_raw"

    configs = datasets.get_dataset_config_names(repo_name)
    for config_name in configs:
        convert_conll2012_config(repo_name, config_name)
