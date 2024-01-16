"""
Convert automatic datasets to parquet.
"""

from pathlib import Path

import datasets
from huggingface_hub import HfApi


api = HfApi()

base_path = Path("dataset_creation/")
automatic_datasets_path = base_path / "automatic"

automatic_datasets = [f for f in automatic_datasets_path.iterdir() if f.is_dir()]


for dataset_path in automatic_datasets:
    repo_name = "coref-data/" + dataset_path.stem
    creation_script_fname = dataset_path.stem + ".py"

    if not api.repo_exists(repo_name, repo_type="dataset"):
        print(f"{repo_name} does not exist.")
        continue

    if not api.file_exists(repo_name, creation_script_fname, repo_type="dataset"):
        print(f"{repo_name} dataset creation script does not exist.")
        continue

    # convert the dataset to parquet
    configs = datasets.get_dataset_config_names(repo_name)
    for config_name in configs:
        dataset = datasets.load_dataset(repo_name, config_name, trust_remote_code=True)
        dataset.push_to_hub(
            repo_name,
            config_name=config_name,
        )

    # delete the dataset creation script
    api.delete_file(
        creation_script_fname,
        repo_id=repo_name,
        repo_type="dataset",
    )
