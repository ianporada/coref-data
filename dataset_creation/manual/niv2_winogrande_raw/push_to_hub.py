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

"""
All "coreference resolution" tasks:

task1391_winogrande_coreference_resolution
task1664_wino_bias_coreference_resolution
task304_numeric_fused_head_coreference_resolution
task892_gap_coreference_resolution
task891_gap_coreference_resolution
task330_gap_coreference_resolution
task401_numeric_fused_head_coreference_resolution
task033_winogrande_coreference_resolution
task133_winowhy_coreference_resolution
task329_gap_coreference_resolution
task249_enhanced_wsc_coreference_resolution
task648_winograd_wsc_coreference_resolution
task1390_wsc_fiexed_coreference_resolution
task893_gap_coreference_resolution
"""

dataset = datasets.load_dataset("DataProvenanceInitiative/niv2_submix_original")

winogrande_dataset = dataset.filter(lambda example: 'winogrande' in example["task_name"])

winogrande_dataset.push_to_hub("coref-data/niv2_winogrande_raw")
