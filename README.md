# coref-data
A collection of coreference annotations.

## Overview

The purpose of this project is to make coreference annotations more easily usable for research purposes.

## Dataset creation

The creation of each dataset is fully described within this repo and should be reproducible other than obtaining the original data for certain copyrighted datasets.

### Stage 1: Parse raw datasets into HuggingFace datasets

#### Stage 1.1: Obtain the raw datasets

All datasets were manually downloaded in their original format and added to the private repo `hf:coref-data/all_raw_datasets`. This is the original source of each dataset except in those cases where the dataset was already available on HuggingFace.

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

<!-- `hf.co:coref-data/all_raw_datasets` (private repository) contains a backup of the original dataset -->