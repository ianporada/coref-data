"""
Write the raw corefud dataset to the HuggingFace Hub.
"""

import copy
import glob
import os
import re

from datasets import Dataset, DatasetDict
from udapi.block.read.conllu import Conllu as ConlluReader

DATA_DIR = "CorefUD-1.1-public/data/"


def read_docs(conllu_fname):
    raw_docs = ConlluReader(files=conllu_fname, split_docs=True).read_documents()

    docs = []
    for raw_doc in raw_docs:

        doc_id = raw_doc.meta['docname']

        sentences = []

        # sent_id
        for node in raw_doc.nodes_and_empty:

            # for the first node in the tree, create a new sentence
            if not sentences or node.root.sent_id != sentences[-1]["sent_id"]:
                root = node.root
                speaker = None
                match = re.search("^ speaker = (.+)", root.comment, re.M)
                if match:
                    speaker = match.group(1)
                
                sentence = {
                    'sent_id': root.sent_id,
                    'text': root.text,
                    'newpar': root.newpar,
                    'newdoc': root.newdoc,
                    'global_entity': root.document.meta.get('global.Entity'),
                    'comment': root.comment,
                    'speaker': speaker,
                    'tokens': [],
                }
                sentences.append(sentence)

            coref_mentions = []
            for mention in set(node.coref_mentions):
                coref_mentions.append({
                    'span': mention.span,
                    'other': str(mention.other),
                    'eid': mention.entity.eid,
                    'eid_or_grp': mention.entity.eid_or_grp,
                    'etype': mention.entity.etype,
                })

            token = {
                'ord': node.ord,
                'form': node.form,
                'lemma': node.lemma,
                'upos': node.upos,
                'xpos': node.xpos,
                'feats': str(node.feats),
                'head': node.parent.ord if node.parent else None,
                'deprel': node.deprel,
                'coref_mentions': coref_mentions,
            }
            sentences[-1]['tokens'].append(token)

        coref_entities = [
            [{
                "sent_id": mention.head.root.sent_id,
                "span": mention.span,
            } for mention in entity.mentions]
            for entity in raw_doc.coref_entities 
        ]

        doc = {
            "doc_id": doc_id,
            "sentences": sentences,
            "coref_entities": coref_entities,
        }
        docs.append(doc)

    return docs


subset_to_dataset = {}

for dataset_path in glob.glob(os.path.join(DATA_DIR, "CorefUD_*/")):
    train_fname = glob.glob(os.path.join(dataset_path, "*-train.conllu"))[0]
    dev_fname = glob.glob(os.path.join(dataset_path, "*-dev.conllu"))[0]

    dataset_name = os.path.basename(train_fname).replace("-train.conllu", "")

    print(f"Processing {dataset_name}")

    train_docs = read_docs(train_fname)
    validation_docs = read_docs(dev_fname)

    dataset = DatasetDict({
        "train": Dataset.from_list(train_docs),
        "validation": Dataset.from_list(validation_docs),
    })

    subset_to_dataset[dataset_name] = dataset

    print(f"Pushing {dataset_name} to the hub")
    dataset.push_to_hub("coref-data/corefud_raw", dataset_name)


# push all subsets to hub
# for subset, dataset in subset_to_dataset.items():
#     dataset.push_to_hub("coref-data/corefud_raw", subset)
