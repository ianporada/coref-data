---
annotations_creators:
- expert-generated
language:
- en
language_creators:
- expert-generated
license:
- cc-by-4.0
multilinguality:
- monolingual
pretty_name: Modified Winograd Schema Challenge (MWSC)
size_categories:
- n<1K
source_datasets:
- extended|winograd_wsc
task_categories:
- multiple-choice
task_ids:
- multiple-choice-coreference-resolution
paperswithcode_id: null
dataset_info:
  features:
  - name: sentence
    dtype: string
  - name: question
    dtype: string
  - name: options
    sequence: string
  - name: answer
    dtype: string
  splits:
  - name: train
    num_bytes: 11022
    num_examples: 80
  - name: test
    num_bytes: 15220
    num_examples: 100
  - name: validation
    num_bytes: 13109
    num_examples: 82
  download_size: 19197
  dataset_size: 39351
---

# The Modified Winograd Schema Challenge (MWSC)

## Dataset Description

- **Homepage:** [http://decanlp.com](http://decanlp.com)
- **Repository:** https://github.com/salesforce/decaNLP
- **Paper:** [The Natural Language Decathlon: Multitask Learning as Question Answering](https://arxiv.org/abs/1806.08730)
- **Point of Contact:** [Bryan McCann](mailto:bmccann@salesforce.com), [Nitish Shirish Keskar](mailto:nkeskar@salesforce.com)
- **Size of downloaded dataset files:** 19.20 kB
- **Size of the generated dataset:** 39.35 kB
- **Total amount of disk used:** 58.55 kB

### Dataset Summary

Examples taken from the Winograd Schema Challenge modified to ensure that answers are a single word from the context.
This Modified Winograd Schema Challenge (MWSC) ensures that scores are neither inflated nor deflated by oddities in phrasing.

## Dataset Structure

### Data Instances

#### default

- **Size of downloaded dataset files:** 0.02 MB
- **Size of the generated dataset:** 0.04 MB
- **Total amount of disk used:** 0.06 MB

An example looks as follows:
```
{
    "sentence": "The city councilmen refused the demonstrators a permit because they feared violence.",
    "question": "Who feared violence?",
    "options": [ "councilmen", "demonstrators" ],
    "answer": "councilmen"
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- `sentence`: a `string` feature.
- `question`: a `string` feature.
- `options`: a `list` of `string` features.
- `answer`: a `string` feature.

### Data Splits

| name  |train|validation|test|
|-------|----:|---------:|---:|
|default|   80|        82| 100|

### Licensing Information

Our code for running decaNLP has been open sourced under BSD-3-Clause. 

We chose to restrict decaNLP to datasets that were free and publicly accessible for research, but you should check their individual terms if you deviate from this use case.

From the [Winograd Schema Challenge](https://cs.nyu.edu/~davise/papers/WinogradSchemas/WS.html):
> Both versions of the collections are licenced under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).

### Citation Information

If you use this in your work, please cite:
```
@inproceedings{10.5555/3031843.3031909,
  author = {Levesque, Hector J. and Davis, Ernest and Morgenstern, Leora},
  title = {The Winograd Schema Challenge},
  year = {2012},
  isbn = {9781577355601},
  publisher = {AAAI Press},
  abstract = {In this paper, we present an alternative to the Turing Test that has some conceptual and practical advantages. A Wino-grad schema is a pair of sentences that differ only in one or two words and that contain a referential ambiguity that is resolved in opposite directions in the two sentences. We have compiled a collection of Winograd schemas, designed so that the correct answer is obvious to the human reader, but cannot easily be found using selectional restrictions or statistical techniques over text corpora. A contestant in the Winograd Schema Challenge is presented with a collection of one sentence from each pair, and required to achieve human-level accuracy in choosing the correct disambiguation.},
  booktitle = {Proceedings of the Thirteenth International Conference on Principles of Knowledge Representation and Reasoning},
  pages = {552–561},
  numpages = {10},
  location = {Rome, Italy},
  series = {KR'12}
}

@article{McCann2018decaNLP,
  title={The Natural Language Decathlon: Multitask Learning as Question Answering},
  author={Bryan McCann and Nitish Shirish Keskar and Caiming Xiong and Richard Socher},
  journal={arXiv preprint arXiv:1806.08730},
  year={2018}
}
```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@lewtun](https://github.com/lewtun), [@ghomasHudson](https://github.com/ghomasHudson), [@lhoestq](https://github.com/lhoestq) for adding this dataset.