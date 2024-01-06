import datasets
dataset = datasets.load_dataset("DataProvenanceInitiative/niv2_submix_original", cache_dir="~/Downloads/huggingface/")

filtered_dataset = dataset.filter(lambda example: 'wino' in example["task_name"])

winogrande_dataset = filtered_dataset.filter(lambda example: 'winogrande' in example["task_name"])

{
    'task029_winogrande_full_object', # Creating a pair of fill in the blank question-answer pairs on objects.	
    'task030_winogrande_full_person', # Creating a pair of fill in the blank questions on persons.	
    'task031_winogrande_question_generation_object', # Writing a fill in the blank question on objects.	
    'task032_winogrande_question_generation_person', # Writing a fill in the blank question on persons.	
    'task033_winogrande_answer_generation', # Answering a fill in the blank question on objects.	# only debiased
    'task034_winogrande_question_modification_object', # Modifying a fill in the blank question on objects.	
    'task035_winogrande_question_modification_person', # Modifying a fill in the blank question on persons.	
    'task1391_winogrande_easy_answer_generation', # Answering a fill in the blank question on objects.	
 }



f = ds.filter(lambda example:  'task031_winogrande_question_generation_object' == example["task_name"])

import datasets
wsc = datasets.load_dataset("super_glue", 'wsc', cache_dir="~/Downloads/huggingface/")
fixed = datasets.load_dataset("super_glue", 'wsc.fixed', cache_dir="~/Downloads/huggingface/")


wf = wsc.filter(lambda example: 'Kamenev' in example["text"])
ff = fixed.filter(lambda example: 'Kamenev' in example["text"])
#### 

from huggingface_hub import create_repo
create_repo("coref-data/superglue_wsc", repo_type="dataset", private=True)

from huggingface_hub import HfApi
api = HfApi()

api.upload_file(
    path_or_fileobj="/Users/ianporada/Research/code/coref-data/preprocessing/dataset_scripts/superglue_wsc/superglue_wsc.py",
    path_in_repo="superglue_wsc.py",
    repo_id="coref-data/superglue_wsc",
    repo_type="dataset",
)

api.delete_file(
    path_in_repo="superglue_wsc.py",
    repo_id="coref-data/superglue_wsc",
    repo_type="dataset",
)

####

from huggingface_hub import create_repo
create_repo("coref-data/davis_pdp", repo_type="dataset", private=True)

from huggingface_hub import HfApi
api = HfApi()

api.upload_file(
    path_or_fileobj="/Users/ianporada/Research/code/coref-data/preprocessing/dataset_scripts/davis_pdp.py",
    path_in_repo="davis_pdp.py",
    repo_id="coref-data/davis_pdp",
    repo_type="dataset",
)

####

from huggingface_hub import create_repo
create_repo("coref-data/conll2012_ontonotesv5", repo_type="dataset", private=True)

from huggingface_hub import HfApi
api = HfApi()

api.upload_file(
    path_or_fileobj="/Users/ianporada/Research/code/coref-data/preprocessing/dataset_scripts/conll2012_ontonotesv5.py",
    path_in_repo="conll2012_ontonotesv5.py",
    repo_id="coref-data/conll2012_ontonotesv5",
    repo_type="dataset",
)



###
