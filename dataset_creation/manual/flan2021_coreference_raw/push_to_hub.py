"""
Copy the coreference tasks from an existing HuggingFace dataset of Flan2021
"""

import datasets


COREFERENCE_TASK_NAMES = {
    'definite_pronoun_resolution:1.1.0',
    'glue/wnli:2.0.0',
    'super_glue/wsc.fixed:1.0.2',
    'winogrande:1.1.0',
}

dataset = datasets.load_dataset("DataProvenanceInitiative/flan2021_submix_original")

dataset = dataset.filter(lambda example: example["task_name"] in COREFERENCE_TASK_NAMES)

dataset.push_to_hub("coref-data/flan2021_coreference_raw")
