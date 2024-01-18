"""
Convert all conll 2012 configs to indiscrim format
"""

import datasets


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


def convert_conll2012_config(repo_name, config_name):
    dataset = datasets.load_dataset(repo_name, config_name)

    # split each document into the annotated parts
    dataset.map(
        split_doc_into_doc_parts,
        batched=True,
        batch_size=1
    )

    # reformat


def convert_conll2012():
    # convert each config
    repo_name = "coref-data/conll2012_raw"
    configs = datasets.get_dataset_config_names(repo_name)
    for config_name in configs:
        convert_conll2012_config(repo_name, config_name)
        

    document_parts = 