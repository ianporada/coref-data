"""
Write the winogrande recast as coref dataset to the HuggingFace Hub.
"""

from pathlib import Path

import conll_transform
from datasets import Dataset, DatasetDict
from nltk.tokenize.treebank import TreebankWordDetokenizer
from stanza.utils.conll import CoNLL

DATA_DIR = Path("conllu/")

split_to_fname = {"train": "train", "validation": "dev"}

detokenizer = TreebankWordDetokenizer()


def read_conllu_file(fname):
    docs = []
    for doc_name, sentences in conll_transform.read_file(fname).items():
        try:
            coref_chains = conll_transform.compute_chains(sentences)
        except:
            print(f"{doc_name} compute chains failed at file {fname}")
            raise

        # returns doc_dict, doc_empty where doct_empty is words w/o id
        conll_dict, _ = CoNLL.convert_conll(sentences)

        raw_sentences = [[line["text"] for line in sentence] for sentence in conll_dict]
        detokenized_sentences = [detokenizer.detokenize(s) for s in raw_sentences]

        formatted_sentences = []
        for i, sentence in enumerate(conll_dict):
            formatted_sentences.append({
                "id": i,
                "text": detokenized_sentences[i],
                "speaker": None,
                "tokens": sentence,
            })

        docs.append({
            "id": doc_name,
            "genre": "crowdsourced",
            "text": " ".join(detokenized_sentences),

            "sentences": formatted_sentences,

            "coref_chains": coref_chains,

            "meta_data": {
                "comment": "syntax_annotations=stanza|tokenizer=stanza|detokenizer=nltk",
            },
        })
    return docs


# Read data from conll files as one config

dataset_dict = {}
for split, fname_stem in split_to_fname.items():
    docs = read_conllu_file(DATA_DIR / f"{fname_stem}.conll")
    
    dataset_dict[split] = Dataset.from_list(docs)

    dataset = DatasetDict(dataset_dict)

dataset.push_to_hub("coref-data/winogrande_coref")
