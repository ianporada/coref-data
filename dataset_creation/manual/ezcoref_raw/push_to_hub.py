"""
Write the raw ezcoref to huggingface
"""

import json
from pathlib import Path


from datasets import Dataset


data_path = Path("ezCoref/Data/")


def get_examples(config):
    examples = []
    for document_path in (data_path / config).iterdir():

        document_name = document_path.stem
        for part_path in document_path.glob("*.json"):
            part_name = part_path.stem
            with open(part_path) as f:
                data = json.load(f)
            
            examples.append({
                "document_name": document_name,
                "part_name": part_name,
                "data": data,
            })
    return examples


# Upload gold data

config = "gold_data"
dataset = Dataset.from_list(get_examples(config)) 
dataset.push_to_hub("coref-data/ezcoref_raw", config_name=config)

# Upload annotations

config = "annotations"
dataset = Dataset.from_list(get_examples(config)) 
dataset.push_to_hub("coref-data/ezcoref_raw", config_name=config)
