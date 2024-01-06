from huggingface_hub import create_repo
create_repo("coref-data/raw-datasets", repo_type="dataset", private=True)

from huggingface_hub import HfApi
api = HfApi()

api.upload_folder(
    folder_path="~/Downloads/raw-datasets/",
    repo_id="coref-data/raw-datasets",
    repo_type="dataset",
)

