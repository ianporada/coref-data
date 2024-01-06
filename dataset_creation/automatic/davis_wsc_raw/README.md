---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
language:
- en
license:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- n<1K
source_datasets:
- original
task_categories:
- multiple-choice
task_ids:
- multiple-choice-coreference-resolution
paperswithcode_id: wsc
pretty_name: Winograd Schema Challenge
dataset_info:
- config_name: wsc285
  features:
  - name: text
    dtype: string
  - name: pronoun
    dtype: string
  - name: pronoun_loc
    dtype: int32
  - name: quote
    dtype: string
  - name: quote_loc
    dtype: int32
  - name: options
    sequence: string
  - name: label
    dtype:
      class_label:
        names:
          '0': '0'
          '1': '1'
  - name: source
    dtype: string
  splits:
  - name: test
    num_bytes: 52281
    num_examples: 285
  download_size: 113235
  dataset_size: 52281
- config_name: wsc273
  features:
  - name: text
    dtype: string
  - name: pronoun
    dtype: string
  - name: pronoun_loc
    dtype: int32
  - name: quote
    dtype: string
  - name: quote_loc
    dtype: int32
  - name: options
    sequence: string
  - name: label
    dtype:
      class_label:
        names:
          '0': '0'
          '1': '1'
  - name: source
    dtype: string
  splits:
  - name: test
    num_bytes: 49674
    num_examples: 273
  download_size: 113235
  dataset_size: 49674
---

# The original Winograd Schema Challenge (WSC) as hosted by Ernest Davis

## Dataset Description

- **Homepage:** https://cs.nyu.edu/faculty/davise/papers/WinogradSchemas/WS.html
- **Paper:** https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.729.9814&rep=rep1&type=pdf

### Dataset Summary

A Winograd schema is a pair of sentences that differ in only one or two words and that contain an ambiguity that is
resolved in opposite ways in the two sentences and requires the use of world knowledge and reasoning for its
resolution. The schema takes its name from a well-known example by Terry Winograd:

> The city councilmen refused the demonstrators a permit because they [feared/advocated] violence.

If the word is "feared", then "they" presumably refers to the city council; if it is "advocated" then "they"
presumably refers to the demonstrators.

## Dataset Structure

### Data Instances

Each instance contains a text passage with a designated pronoun and two possible answers indicating which entity in
the passage the pronoun represents. An example instance looks like the following:

```python
{
  'label': 0,
  'options': ['The city councilmen', 'The demonstrators'],
  'pronoun': 'they',
  'pronoun_loc': 63,
  'quote': 'they feared violence',
  'quote_loc': 63,
  'source': '(Winograd 1972)',
  'text': 'The city councilmen refused the demonstrators a permit because they feared violence.'
}
 ```

### Data Fields

- `text` (str): The text sequence
- `options` (list[str]): The two entity options that the pronoun may be referring to
- `label` (int): The index of the correct option in the `options` field
- `pronoun` (str): The pronoun in the sequence to be resolved
- `pronoun_loc` (int): The starting position of the pronoun in the sequence
- `quote` (str): The substr with the key action or context surrounding the pronoun
- `quote_loc` (int): The starting position of the quote in the sequence
- `source` (str): A description of the source who contributed the example

### Licensing Information

This work is licensed under a [Creative Commons Attribution 4.0 International
License](https://creativecommons.org/licenses/by/4.0/).

### Citation Information

The Winograd Schema Challenge including many of the examples here was proposed by
[Levesque et al 2012](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.729.9814&rep=rep1&type=pdf):

```
@inproceedings{levesque2012winograd,
  title={The winograd schema challenge},
  author={Levesque, Hector and Davis, Ernest and Morgenstern, Leora},
  booktitle={Thirteenth International Conference on the Principles of Knowledge Representation and Reasoning},
  year={2012},
  organization={Citeseer}
}
```
### Contributions

Thanks to [@joeddav](https://github.com/joeddav) for adding this dataset.