"""
Copy the Winogrande tasks from an existing HuggingFace dataset of Super-Natural Instructions.
"""

import datasets


_WINOGRANDE_TASK_NAMES = {
    'task029_winogrande_full_object', # Creating a pair of fill in the blank question-answer pairs on objects.	
    'task030_winogrande_full_person', # Creating a pair of fill in the blank questions on persons.	
    'task031_winogrande_question_generation_object', # Writing a fill in the blank question on objects.	
    'task032_winogrande_question_generation_person', # Writing a fill in the blank question on persons.	
    'task033_winogrande_answer_generation', # Answering a fill in the blank question on objects.	# only debiased
    'task034_winogrande_question_modification_object', # Modifying a fill in the blank question on objects.	
    'task035_winogrande_question_modification_person', # Modifying a fill in the blank question on persons.	
    'task1391_winogrande_easy_answer_generation', # Answering a fill in the blank question on objects.	
}

dataset = datasets.load_dataset("DataProvenanceInitiative/niv2_submix_original")

winogrande_dataset = dataset.filter(lambda example: 'winogrande' in example["task_name"])

winogrande_dataset.push_to_hub("coref-data/niv2_winogrande_raw")
