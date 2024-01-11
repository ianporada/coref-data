"""
Copy the coreference tasks from an existing HuggingFace dataset of Super-Natural Instructions.
"""

import datasets


COREFERENCE_TASK_NAMES = {
    "task1391_winogrande_coreference_resolution",
    "task1664_wino_bias_coreference_resolution",
    "task304_numeric_fused_head_coreference_resolution",
    "task892_gap_coreference_resolution",
    "task891_gap_coreference_resolution",
    "task330_gap_coreference_resolution",
    "task401_numeric_fused_head_coreference_resolution",
    "task033_winogrande_coreference_resolution",
    "task133_winowhy_coreference_resolution",
    "task329_gap_coreference_resolution",
    "task249_enhanced_wsc_coreference_resolution",
    "task648_winograd_wsc_coreference_resolution",
    "task1390_wsc_fiexed_coreference_resolution",
    "task893_gap_coreference_resolution",
}

dataset = datasets.load_dataset("DataProvenanceInitiative/niv2_submix_original")

dataset = dataset.filter(lambda example: example["task_name"] in COREFERENCE_TASK_NAMES)

dataset.push_to_hub("coref-data/niv2_coreference_raw", private=True)
