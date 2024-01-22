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
from indiscrim_conversion.preco import convert_preco
from indiscrim_conversion.litbank import convert_litbank
from indiscrim_conversion.gum import convert_gum
from indiscrim_conversion.corefud import convert_corefud
from indiscrim_conversion.arrau import convert_arrau

api = HfApi()
fs = HfFileSystem()


README_TEMPLATE = """
This dataset was generated by reformatting [`%s`](https://huggingface.co/datasets/%s) into the indiscrim coreference format. See that repo for dataset details.

See [ianporada/coref-data](https://github.com/ianporada/coref-data) for additional conversion details and the conversion script.

Please create an issue in the repo above or in this dataset repo for any questions.
"""

def update_readme_file(repo_name, old_repo_name=None):
    """append a short description to the repo README"""
    assert api.repo_exists(repo_name, repo_type="dataset"), f"{repo_name} does not exist"
    readme_fname = f"datasets/{repo_name}/README.md"

    # would be better to use existing yaml parser at `datasets.utils.metadata.MetadataConfigs`
    old_readme_text = fs.read_text(readme_fname)
    yaml_meta_data = old_readme_text[:old_readme_text.rindex("---")]
    new_readme_text = yaml_meta_data + "---\n" + README_TEMPLATE % (old_repo_name, old_repo_name)

    with fs.open(f"datasets/{repo_name}/README.md", "w") as f:
        f.write(new_readme_text)


def convert_raw_to_indiscrim(repo_name, conversion_function, overwrite=False):
    """call each conversion function"""
    if not overwrite and api.repo_exists(repo_name, repo_type="dataset"):
        return
    print(f"Converting dataset {repo_name}")
    conversion_function()

    new_repo_name = repo_name.replace("_raw", "_indiscrim")
    update_readme_file(new_repo_name, old_repo_name=repo_name)


def main():
    # convert all datasets
    # for repo_name, conversion_function in repo_to_conversion_fn.items():

    # convert_raw_to_indiscrim("coref-data/conll2012_raw", convert_conll2012)
    # convert_raw_to_indiscrim("coref-data/preco_raw", convert_preco)
    # convert_raw_to_indiscrim("coref-data/litbank_raw", convert_litbank)
    # convert_raw_to_indiscrim("coref-data/gum_raw", convert_gum)
    # convert_raw_to_indiscrim("coref-data/corefud_raw", convert_corefud)
    convert_raw_to_indiscrim("coref-data/arrau_raw", convert_arrau, True)





if __name__ == "__main__":
    main()