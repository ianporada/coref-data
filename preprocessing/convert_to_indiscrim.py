"""
Convert raw datasets into the "indiscrim" (indiscriminate) coreference format

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
  "genre": str,
  "meta_data": {
      "comment": str,
  },
}
"""

from huggingface_hub import HfApi, HfFileSystem

from indiscrim_conversion.conll2012 import convert_conll2012

api = HfApi()
fs = HfFileSystem()

repo_to_conversion_fn = {
    "coref-data/conll2012_raw": convert_conll2012,
}


def update_readme_file(repo_name):
    """add a short description to the repo"""
    assert api.repo_exists(repo_name, repo_type="dataset"), f"{repo_name} does not exist"

    with fs.open(f"datasets/{repo_name}/README.md", "a") as f:
        


def convert_raw_to_indiscrim():
    """call each conversion function"""
    for repo_name, conversion_function in repo_to_conversion_fn.items():
        if api.repo_exists(repo_name, repo_type="dataset"):
            continue
        print(f"Converting dataset {repo_name}")
        conversion_function()

        new_repo_name = repo_name.replace("_raw", "_indiscrim")
        update_readme_file(new_repo_name)




def main():
    # convert all datasets
    convert_raw_to_indiscrim()

    update_readme_files()


if __name__ == "__main__":
    main()