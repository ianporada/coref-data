---
license: apache-2.0
---

# Dataset Card for "gap"

## Dataset Description

- **Homepage:** [https://github.com/google-research-datasets/gap-coreference](https://github.com/google-research-datasets/gap-coreference)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [Mind the GAP: A Balanced Corpus of Gendered Ambiguous Pronouns](https://arxiv.org/abs/1810.05201)
- **Point of Contact:** [gap-coreference@google.com](mailto:gap-coreference@google.com)
- **Size of downloaded dataset files:** 2.40 MB
- **Size of the generated dataset:** 2.43 MB
- **Total amount of disk used:** 4.83 MB

### Dataset Summary

GAP is a gender-balanced dataset containing 8,908 coreference-labeled pairs of
(ambiguous pronoun, antecedent name), sampled from Wikipedia and released by
Google AI Language for the evaluation of coreference resolution in practical
applications.

## Dataset Structure

### Data Instances

#### default

- **Size of downloaded dataset files:** 2.40 MB
- **Size of the generated dataset:** 2.43 MB
- **Total amount of disk used:** 4.83 MB

An example of 'validation' looks as follows.
```
{
    "A": "aliquam ultrices sagittis",
    "A-coref": false,
    "A-offset": 208,
    "B": "elementum curabitur vitae",
    "B-coref": false,
    "B-offset": 435,
    "ID": "validation-1",
    "Pronoun": "condimentum mattis pellentesque",
    "Pronoun-offset": 948,
    "Text": "Lorem ipsum dolor",
    "URL": "sem fringilla ut"
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- `ID`: a `string` feature.
- `Text`: a `string` feature.
- `Pronoun`: a `string` feature.
- `Pronoun-offset`: a `int32` feature.
- `A`: a `string` feature.
- `A-offset`: a `int32` feature.
- `A-coref`: a `bool` feature.
- `B`: a `string` feature.
- `B-offset`: a `int32` feature.
- `B-coref`: a `bool` feature.
- `URL`: a `string` feature.

### Data Splits

| name  |train|validation|test|
|-------|----:|---------:|---:|
|default| 2000|       454|2000|


### Citation Information

```
@article{webster-etal-2018-mind,
    title = "Mind the {GAP}: A Balanced Corpus of Gendered Ambiguous Pronouns",
    author = "Webster, Kellie  and
      Recasens, Marta  and
      Axelrod, Vera  and
      Baldridge, Jason",
    journal = "Transactions of the Association for Computational Linguistics",
    volume = "6",
    year = "2018",
    address = "Cambridge, MA",
    publisher = "MIT Press",
    url = "https://aclanthology.org/Q18-1042",
    doi = "10.1162/tacl_a_00240",
    pages = "605--617",
}
```

### Contributions

Modified from dataset added by [@thomwolf](https://github.com/thomwolf), [@patrickvonplaten](https://github.com/patrickvonplaten), [@otakumesi](https://github.com/otakumesi), [@lewtun](https://github.com/lewtun)