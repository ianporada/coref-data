---
license: cc-by-4.0
---

# The Knowref 60K Dataset

The second version of the Knowref dataset.
From: https://github.com/aemami1/KnowRef60k

## Fields

- `annotation_strength` (str): annotator agreement from 1-5
- `candidate_0` (str): the first candidate name
- `candidate_1` (str): the second candidate name
- `original_sentence` (str): sentence before swapping the names
- `swapped_sentence` (str): sentence after swapping the names with square brackets marking the pronoun
- `correct_candidate` (str): either "candidate_0" or "candidate_1"


Citation:
```
@inproceedings{emami-etal-2020-analysis,
    title = "An Analysis of Dataset Overlap on {W}inograd-Style Tasks",
    author = "Emami, Ali  and
      Suleman, Kaheer  and
      Trischler, Adam  and
      Cheung, Jackie Chi Kit",
    editor = "Scott, Donia  and
      Bel, Nuria  and
      Zong, Chengqing",
    booktitle = "Proceedings of the 28th International Conference on Computational Linguistics",
    month = dec,
    year = "2020",
    address = "Barcelona, Spain (Online)",
    publisher = "International Committee on Computational Linguistics",
    url = "https://aclanthology.org/2020.coling-main.515",
    doi = "10.18653/v1/2020.coling-main.515",
    pages = "5855--5865",
    abstract = "The Winograd Schema Challenge (WSC) and variants inspired by it have become important benchmarks for common-sense reasoning (CSR). Model performance on the WSC has quickly progressed from chance-level to near-human using neural language models trained on massive corpora. In this paper, we analyze the effects of varying degrees of overlaps that occur between these corpora and the test instances in WSC-style tasks. We find that a large number of test instances overlap considerably with the pretraining corpora on which state-of-the-art models are trained, and that a significant drop in classification accuracy occurs when models are evaluated on instances with minimal overlap. Based on these results, we provide the WSC-Web dataset, consisting of over 60k pronoun disambiguation problems scraped from web data, being both the largest corpus to date, and having a significantly lower proportion of overlaps with current pretraining corpora.",
}
```