### Stage 1: Parse raw datasets into HuggingFace datasets

#### Stage 1.1: Obtain the raw datasets

All datasets were manually downloaded in their original format and added to the private repo `hf.co:coref-data/all_raw_datasets`. This is the original source of each dataset except in those cases where the dataset was already available on HuggingFace.

#### Stage 1.2: Upload the datasets to HuggingFace

Some datasets (those in `dataset_creation/automatic`) were created using HuggingFace dataset creation scripts. This can be reproduced by running the following scripts to create the datasets and convert them to parquet format. (In order to enable the dataset viewer, the datasets needed to be converted to a format such as parquet.)

Create automatic datasets that do not exist, and convert all automatic datasets to parquet:

```
python dataset_creation/create_automatic_datasets.py
python dataset_creation/convert_datasets_to_parquet.py
```

All other datasets (those in `dataset_creation/manual`) were created by uploading the original dataset to HuggingFace. If a given dataset required preprocessing in order to be uploaded, this preprocessing code is available in the corresponding dataset directory at `dataset_creation/manual/$DATASET_NAME/push_to_hub.py`. Running this `push_to_hub.py` script from inside the corresponding original dataset directory will upload the raw dataset to HuggingFace.

For example, to manually create the mmc dataset (assuming the corpus and repos exist at these particular paths):
```
cd ~/Research/data/push_to_hub/mmc/
python ~/Research/code/coref-data/dataset_creation/manual/mmc_raw/push_to_hub.py
```

README.md files for each dataset can be updated by running
```
python dataset_creation/update_readme_files.py
```