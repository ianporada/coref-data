# coref-data
A collection of coreference annotations.

## Overview

The purpose of this project is to make coreference annotations more easily usable for research purposes.

## Dataset creation

The creation of each dataset is fully described within this repo and should be reproducible other than obtaining the original data for certain copyrighted datasets.

### Stage 1: Parse raw datasets into HuggingFace datasets

#### Stage 1.1: Obtain the raw datasets

All datasets were manually downloaded in their original format and added to the private repo `hf.co:coref-data/all_raw_datasets`. This is the original source of each dataset except in those cases where the dataset was already available on HuggingFace.

#### Stage 1.2: Upload the datasets to HuggingFace

Some datasets (those in `dataset_creation/automatic`) were created using HuggingFace dataset creation scripts. This can be reproduced by running the following scripts to create the datasets and convert them to parquet format. (In order to enable the dataset viewer, the datasets needed to be converted to a format such as parquet.)

Update README files for all datasets, create automatic datasets that do not exist, and convert all automatic datasets to parquet:
```
python dataset_creation/create_automatic_datasets.py
python dataset_creation/convert_datasets_to_parquet.py
```

All other datasets (those in `dataset_creation/manual`) were created by manually uploading the original dataset. Running the above scripts will only update the README.md file for such datasets. If a given dataset required preprocessing in order to be uploaded to HuggingFace, this preprocessing code is available in the corresponding dataset directory at `dataset_creation/manual/$DATASET_NAME/push_to_hub.py`. Running this `push_to_hub.py` script from inside the corresponding original dataset directory will upload the raw dataset to HuggingFace.

For example, to manually create the mmc dataset (assuming the corpus and repos exist at these particular paths):
```
cd ~/Research/data/push_to_hub/mmc/
python ~/Research/code/coref-data/dataset_creation/manual/mmc_raw/push_to_hub.py
```

README.md files for each dataset can be updated by running
```
python dataset_creation/update_readme_files.py
```

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
      "id": int, # sentence index
      "text": str, # untokenized sentence text
      "speaker": None, # speaker
      "tokens": [
        {
          # keys are conllu columns: id, text, lemma, upos, xpos, feats, head, deprel, deps, misc
        },
        ...
      ]
    },
    ...
  ],
  "coref_chains": List[List[List[int]]], # list of clusters, each cluster is a list of mentions, each mention is a span represented as [sent, start, end] inclusive
  "genre": str, # a string describing the genre of text
  "meta_data": {
      "comment": str, # meta details about the dataset instance
  },
}
```