"""
Write the raw korean_ecmt dataset to the HuggingFace Hub.

The original text should be recoverable from the dataset at https://github.com/machinereading/crowdsourcing
"""

import datasets
from stanza.utils.conll import CoNLL


# data files are available at this URL
DATA_URL = "https://github.com/machinereading/CR/blob/743f758e2b0c1fad6a06ce600b59ae882ab66c0e/input/"

TRAIN_FNAME = "nonJosa_train1345.NER5.v4_gold_conll"
VALIDATION_FNAME = "nonJosa_dev.NER5.v4_gold_conll"
TEST_FNAME = "whole.korean8_pd_NER.v4_gold_conll"

fname = TEST_FNAME

doc = CoNLL.conll2doc(fname)
data = doc.to_dict()


dataset = datasets.load_dataset("DataProvenanceInitiative/niv2_submix_original")

winogrande_dataset = dataset.filter(lambda example: 'winogrande' in example["task_name"])

winogrande_dataset.push_to_hub("coref-data/niv2_winogrande_raw")
