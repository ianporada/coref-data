# coref-data
A collection of coreference annotations.

## Overview

The purpose of this project is to make coreference annotations more easily usable for research purposes.

## Dataset creation

The creation of each dataset is fully described within this repo and should be reproducible other than obtaining the original data for certain copyrighted datasets.

### Stage 1: Parse raw datasets into HuggingFace datasets

First, the raw datasets were downloaded and then uploaded to the HuggingFace with minimal formatting. To reproduce these steps, see: [dataset_creation/README.md](dataset_creation/README.md).

### Stage 2: Convert raw HuggingFace datasets into unified formats

#### Indiscrim Format

Coreference is often treated as the indiscriminate clustering of textual spans. 
Portions of certain datasets that be represented this way have been converted to a unfied format, referred to as the "indiscrim" format.
The [Indiscriminate Identity Coreference](https://huggingface.co/collections/coref-data/indiscriminate-identity-coreference-65a7f336c46ce42ef5655570) collection on HuggingFace hub as a list of datasets in this format.

Converting datasets to indiscrim format can be reproduced by running the following command:

```python
python preprocessing/convert_to_indiscrim.py
```

The format is as follows:

```python
{
  "id": str, # example id
  "text": str, # untokenized example text
  "sentences": [
    {
      "id": int, # sentence id (starting at 1 unless the first token is a zero/ellipsis)
      "text": str, # untokenized sentence text, may also have attributes start_char and end_char
      "speaker": None, # speaker
      "tokens": [
        {
          # keys are conllu columns: id, text, lemma, upos, xpos, feats, head, deprel, deps, misc
          # start_char and end_char may also be included
        },
        ...
      ]
    },
    ...
  ],
  "coref_chains": List[List[List[int]]], # list of clusters, each cluster is a list of mentions, each mention is a span represented as [sent, local_start, local_end] inclusive indices
  "genre": str, # a string describing the genre of text
  "meta_data": {
      "comment": str, # meta details about the dataset instance
  },
}
```

#### Reference

This code was originally written for the following project. A significantly updated version will be published at ACL Findings 2024.

```
@misc{porada2023investigating,
    title={Investigating Failures to Generalize for Coreference Resolution Models},
    author={Ian Porada and Alexandra Olteanu and Kaheer Suleman and Adam Trischler and Jackie Chi Kit Cheung},
    year={2023},
    eprint={2303.09092},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
```