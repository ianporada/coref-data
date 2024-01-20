"""
Convert all conll 2012 configs to indiscrim format
"""

import collections
from functools import partial
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
    """from https://github.com/juntaoy/aracoref/blob/main/preprocess_arabic.py"""
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
    return text


def format_sentence(sent_and_index, config=None):
    """format a raw sentence in standardized indiscrim format"""
    index, raw_sentence = sent_and_index
    tokens = [{"text": w} for w in raw_sentence["words"]]

    if config == "arabic_v4":
        

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


def convert_conll2012_config(repo_name, config_name):
    dataset = datasets.load_dataset(repo_name, config_name)

    # split each document into the annotated parts
    dataset = dataset.map(
        split_doc_into_doc_parts,
        batched=True,
        batch_size=1,
    )

    # reformat
    convert_doc = partial(convert_doc_into_indiscrim, config=config_name)
    dataset = dataset.map(
        convert_doc_into_indiscrim,
        batched=True,
        batch_size=1,
    )

    dataset.push_to_hub("coref-data/conll2012_indiscrim", config_name)


def convert_conll2012():
    # convert each config
    repo_name = "coref-data/conll2012_raw"

    configs = datasets.get_dataset_config_names(repo_name)
    for config_name in configs:
        convert_conll2012_config(repo_name, config_name)
