"""Add dependency parse to the given dataset"""

import click
import datasets
import stanza
from datasets import Value, load_dataset
from tqdm import tqdm

datasets_to_parse = [
    ("coref-data/preco_indiscrim", "default"), # 0
    ("coref-data/litbank_indiscrim", "split_0"), # 1
    ("coref-data/arrau_indiscrim", "default"), # 2
    ("coref-data/phrase_detectives_indiscrim", "default"), # 3
    ("coref-data/mmc_indiscrim", "mmc_en"), # 4
    # just constituency
    ("coref-data/gum_indiscrim", "ontogum"), # 5
    ("coref-data/gum_indiscrim", "original"), # 6
    ("coref-data/knowref_60k_indiscrim", "default"), # 7
]

nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma,depparse,constituency', tokenize_pretokenized=True)
# nlp = stanza.Pipeline(lang='en', processors='tokenize,pos,constituency', tokenize_pretokenized=True)


def add_parse_to_example(example, only_constituency=False):
    sentences = example["sentences"]
    words = [[t["text"] for t in s["tokens"]] for s in sentences]
    doc = nlp(words)
    
    for stanza_sentence, sentence in zip(doc.sentences, sentences):
        sentence["misc"] = {"parse_tree": str(stanza_sentence.constituency)}
        if only_constituency:
            continue
        for stanza_word, token in zip(stanza_sentence.words, sentence["tokens"]):
            assert stanza_word.text == token["text"] and stanza_word.id == token["id"]
            word_dict = stanza_word.to_dict()
            for key, value in word_dict.items():
                token[key] = value
    return example


def add_parse(dataset_name, dataset_config, val_test_only=False, test_only=False, num_proc=4):
    dataset = load_dataset(dataset_name, dataset_config)
    # features = dataset["train"].features
    # features["sentences"][0]['misc'] =  {'parse_tree': Value(dtype='string', id=None)}
    if val_test_only:
        dataset = datasets.DatasetDict({
            "validation": dataset["validation"].map(add_parse_to_example, num_proc=num_proc),
            "test": dataset["test"].map(add_parse_to_example, num_proc=num_proc),
        })
        dataset_name += "_parsed"
    if test_only:
        dataset = datasets.DatasetDict({
            "test": dataset["test"].map(add_parse_to_example, num_proc=num_proc),
        })
        dataset_name += "_parsed"
    else:
        dataset = dataset.map(add_parse_to_example, num_proc=num_proc)
    dataset.push_to_hub(dataset_name, dataset_config)


@click.command()
@click.option('--dataset_index', type=int)
@click.option("--val_test_only", is_flag=True, default=False)
@click.option("--test_only", is_flag=True, default=False)
@click.option('--start', default=-1, type=int)
@click.option('--end', default=-1, type=int)
def main(dataset_index, val_test_only, test_only, start, end):
    dataset_name, dataset_config = datasets_to_parse[dataset_index]
    if start < 0:
        add_parse(dataset_name, dataset_config, val_test_only, test_only)
        return
    
    # dataset = load_dataset(dataset_name, dataset_config, split="train")
    # dataset = dataset.sort("id")
    # dataset = dataset.select(range(start, end))
    # dataset = dataset.map(add_parse_to_example, num_proc=8)
    # examples = sorted(examples, key=lambda x: x["id"])


#     if start < 0 and end < 0:
#         dataset = 
#         validation_split = dataset["validation"]
# 

# for example in tqdm(examples):
#     add_parse_to_example(example)


    
if __name__ == '__main__':
    main()
