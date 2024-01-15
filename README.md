# coref-data
A collection of coreference annotations.

## Overview

The purpose of this project is to make coreference annotations more easily usable for research purposes.

## Dataset creation

### Stage 1: Parse raw datasets into HuggingFace datasets

Some datasets (those in `dataset_creation/automatic`) were created using HuggingFace dataset creation scripts. This can be reproduced by running the following scripts to create the datasets and convert them to parquet format. (In order to enable the dataset viewer, the datasets needed to be converted to a format such as parquet.)

```
python dataset_creation/generate_datasets.py
python dataset_creation/convert_datasets_to_parquet.py
```

All other datasets (those in `dataset_creation/manual`) were created by manually uploading the original dataset. Running the above scripts will only update the README.md file for such datasets. If a given dataset required preprocessing in order to be uploaded to HuggingFace, this preprocessing code is available in the corresponding dataset directory at `dataset_creation/manual/$DATASET_NAME/push_to_hub.py`.

### Stage 2: Convert raw HuggingFace datasets into unified formats

<!-- `hf.co:coref-data/all_raw_datasets` (private repository) contains a backup of the original dataset -->