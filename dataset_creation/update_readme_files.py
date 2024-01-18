"""
For each repo in dataset creation, upload the README.md file.
If the repo is in "automatic", also upload the dataset creation script.
"""

from pathlib import Path

from huggingface_hub import HfApi, HfFileSystem

api = HfApi()
fs = HfFileSystem()

base_path = Path("dataset_creation/")
automatic_datasets_path = base_path / "automatic"
manual_datasets_path = base_path / "manual"

automatic_datasets = [f for f in automatic_datasets_path.iterdir() if f.is_dir()]
manual_datasets = [f for f in manual_datasets_path.iterdir() if f.is_dir()]

all_datasets = automatic_datasets + manual_datasets

# First, make sure the dataset exists
for dataset_path in all_datasets:
    repo_name = "coref-data/" + dataset_path.stem

    if not api.repo_exists(repo_name, repo_type="dataset"):
        print(f"Creating dataset {repo_name}")
        api.create_repo(repo_name, repo_type="dataset")

    api.upload_file(
        path_or_fileobj=dataset_path / "README.md",
        path_in_repo="README.md",
        repo_id=repo_name,
        repo_type="dataset",
    )
