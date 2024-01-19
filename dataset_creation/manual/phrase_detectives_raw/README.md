---
license: other
configs:
- config_name: conll
  data_files:
  - split: train
    path: conll/train-*
  - split: dev
    path: conll/dev-*
  - split: test
    path: conll/test-*
- config_name: conll_singletons
  data_files:
  - split: train
    path: conll_singletons/train-*
  - split: dev
    path: conll_singletons/dev-*
  - split: test
    path: conll_singletons/test-*
- config_name: masxml
  data_files:
  - split: train
    path: masxml/train-*
  - split: dev
    path: masxml/dev-*
  - split: test
    path: masxml/test-*
---

# Phrase Detectives Version 3

- Project: https://github.com/dali-ambiguity/Phrase-Detectives-Corpus-3.0
- Data source: https://drive.google.com/file/d/1R72bY6gHyC3amy9VxLjKrougJUxhY_HK/view?usp=sharing

## Details

The Phrase Detectives Corpus v3. Publicly distributed. License: LDC User Agreement for Non-Members (v1 and v2)

## Citation
```
@inproceedings{yu-etal-2023-aggregating,
    title = "Aggregating Crowdsourced and Automatic Judgments to Scale Up a Corpus of Anaphoric Reference for Fiction and {W}ikipedia Texts",
    author = "Yu, Juntao  and
      Paun, Silviu  and
      Camilleri, Maris  and
      Garcia, Paloma  and
      Chamberlain, Jon  and
      Kruschwitz, Udo  and
      Poesio, Massimo",
    editor = "Vlachos, Andreas  and
      Augenstein, Isabelle",
    booktitle = "Proceedings of the 17th Conference of the European Chapter of the Association for Computational Linguistics",
    month = may,
    year = "2023",
    address = "Dubrovnik, Croatia",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.eacl-main.54",
    doi = "10.18653/v1/2023.eacl-main.54",
    pages = "767--781",
    abstract = "Although several datasets annotated for anaphoric reference / coreference exist, even the largest such datasets have limitations in term of size, range of domains, coverage of anaphoric phenomena, and size of documents included. Yet, the approaches proposed to scale up anaphoric annotation haven{'}t so far resulted in datasets overcoming these limitations. In this paper, we introduce a new release of a corpus for anaphoric reference labelled via a game-with-a-purpose. This new release is comparable in size to the largest existing corpora for anaphoric reference due in part to substantial activity by the players, in part thanks to the use of a new resolve-and-aggregate paradigm to {`}complete{'} markable annotations through the combination of an anaphoric resolver and an aggregation method for anaphoric reference. The proposed method could be adopted to greatly speed up annotation time in other projects involving games-with-a-purpose. In addition, the corpus covers genres for which no comparable size datasets exist (Fiction and Wikipedia); it covers singletons and non-referring expressions; and it includes a substantial number of long documents ( 2K in length).",
}
```