---
license: unknown
---

The original PreCo `.jsonl` files from https://preschool-lab.github.io/PreCo/

## What is PreCo?
PreCo is a large-scale English dataset for coreference resolution. The dataset is designed to embody the core challenges in coreference, such as entity representation, by alleviating the challenge of low overlap between training and test sets and enabling separated analysis of mention detection and mention clustering. To strengthen the training-test overlap, we collect a large corpus of 38K documents and 12.5M words which are mostly from the vocabulary of English-speaking preschoolers. Experiments show that with higher training-test overlap, error analysis on PreCo is more efficient than the one on OntoNotes, a popular existing dataset. Furthermore, we annotate singleton mentions making it possible for the first time to quantify the influence that a mention detector makes on coreference resolution performance.

The dataset is available for research purposes.

## Data Format
There are 2 JSON line files in the downloaded data, for training and development sets. We are still in the process of deciding how to use the test set, e.g., to publish it as is, or to hold an online competition. In the files, each line is a JSON string that encodes a document. The JSON object has the following fields:

"id": a string identifier of the document.
"sentences": the text. It is a list of sentences. Each sentence is a list of tokens. Each token is a string, which can be a word or a punctuation mark. A sentence that contains only one token of space is used to separate paragraphs in the text.
"mention_clusters": the mention clusters of the document. It is a list of mention clusters. Each mention cluster is a list of mentions. Each mention is a tuple of integers [sentence_idx, begin_idx, end_idx]. Sentence_idx is the index of the sentence of the mention. Begin_idx is the index of the first token of the mention in the sentence. End_index is the index of the last token of the mention in the sentence plus one. All indices are zero-based.

```
@inproceedings{chen-etal-2018-preco,
    title = "{P}re{C}o: A Large-scale Dataset in Preschool Vocabulary for Coreference Resolution",
    author = "Chen, Hong  and
      Fan, Zhenhua  and
      Lu, Hao  and
      Yuille, Alan  and
      Rong, Shu",
    editor = "Riloff, Ellen  and
      Chiang, David  and
      Hockenmaier, Julia  and
      Tsujii, Jun{'}ichi",
    booktitle = "Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing",
    month = oct # "-" # nov,
    year = "2018",
    address = "Brussels, Belgium",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/D18-1016",
    doi = "10.18653/v1/D18-1016",
    pages = "172--181",
    abstract = "We introduce PreCo, a large-scale English dataset for coreference resolution. The dataset is designed to embody the core challenges in coreference, such as entity representation, by alleviating the challenge of low overlap between training and test sets and enabling separated analysis of mention detection and mention clustering. To strengthen the training-test overlap, we collect a large corpus of 38K documents and 12.5M words which are mostly from the vocabulary of English-speaking preschoolers. Experiments show that with higher training-test overlap, error analysis on PreCo is more efficient than the one on OntoNotes, a popular existing dataset. Furthermore, we annotate singleton mentions making it possible for the first time to quantify the influence that a mention detector makes on coreference resolution performance. The dataset is freely available at \url{https://preschool-lab.github.io/PreCo/}.",
}
```