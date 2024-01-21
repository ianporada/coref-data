---
license: cc-by-4.0
configs:
- config_name: split_0
  data_files:
  - split: train
    path: split_0/train-*
  - split: validation
    path: split_0/validation-*
  - split: test
    path: split_0/test-*
- config_name: split_1
  data_files:
  - split: train
    path: split_1/train-*
  - split: validation
    path: split_1/validation-*
  - split: test
    path: split_1/test-*
- config_name: split_2
  data_files:
  - split: train
    path: split_2/train-*
  - split: validation
    path: split_2/validation-*
  - split: test
    path: split_2/test-*
- config_name: split_3
  data_files:
  - split: train
    path: split_3/train-*
  - split: validation
    path: split_3/validation-*
  - split: test
    path: split_3/test-*
- config_name: split_4
  data_files:
  - split: train
    path: split_4/train-*
  - split: validation
    path: split_4/validation-*
  - split: test
    path: split_4/test-*
- config_name: split_5
  data_files:
  - split: train
    path: split_5/train-*
  - split: validation
    path: split_5/validation-*
  - split: test
    path: split_5/test-*
- config_name: split_6
  data_files:
  - split: train
    path: split_6/train-*
  - split: validation
    path: split_6/validation-*
  - split: test
    path: split_6/test-*
- config_name: split_7
  data_files:
  - split: train
    path: split_7/train-*
  - split: validation
    path: split_7/validation-*
  - split: test
    path: split_7/test-*
- config_name: split_8
  data_files:
  - split: train
    path: split_8/train-*
  - split: validation
    path: split_8/validation-*
  - split: test
    path: split_8/test-*
- config_name: split_9
  data_files:
  - split: train
    path: split_9/train-*
  - split: validation
    path: split_9/validation-*
  - split: test
    path: split_9/test-*
---

# LitBank

- Project: https://github.com/dbamman/litbank
- Data source: https://github.com/dbamman/litbank/commit/3e50db0ffc033d7ccbb94f4d88f6b99210328ed8
- Crossval splits source: https://github.com/dbamman/lrec2020-coref/commit/e30de53743d36d1ea2c9e7292c69477fa332713c

## Details

Ten configs of the form f"split_{X}" where X is in range(10)

### Features

```
{'coref_chains': List[List[List[int]]] # list of clusters, each cluster is a list of mentions, each mention is a list of [sent_idx, start, end] inclusive
 'doc_name': str
 'entities': List[List[{'bio_tags': List[str]
                        'token': str}]], # list of sentences, each sentence is a list of tokens, each token has a list of bio tags and the token
 'events': List[List[{'is_event': bool,
                      'token': str}]], # list of sentences, each sentence is a list of tokens, each token contains is_event and the token
 'meta_info': {'author': str,
               'date': str,
               'gutenberg_id': str,
               'title': str},
 'original_text': str,
 'quotes': List[{'attribution': str,
             'end': {'sent_id': str,
                     'token_id': str},
             'quotation': str,
             'quote_id': str,
             'start': {'sent_id': str,
                       'token_id': str}}],
 'sentences': List[List[str]],
}
```

## Citation
```
@inproceedings{bamman-etal-2019-annotated,
    title = "An annotated dataset of literary entities",
    author = "Bamman, David  and
      Popat, Sejal  and
      Shen, Sheng",
    editor = "Burstein, Jill  and
      Doran, Christy  and
      Solorio, Thamar",
    booktitle = "Proceedings of the 2019 Conference of the North {A}merican Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)",
    month = jun,
    year = "2019",
    address = "Minneapolis, Minnesota",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/N19-1220",
    doi = "10.18653/v1/N19-1220",
    pages = "2138--2144",
    abstract = "We present a new dataset comprised of 210,532 tokens evenly drawn from 100 different English-language literary texts annotated for ACE entity categories (person, location, geo-political entity, facility, organization, and vehicle). These categories include non-named entities (such as {``}the boy{''}, {``}the kitchen{''}) and nested structure (such as [[the cook]{'}s sister]). In contrast to existing datasets built primarily on news (focused on geo-political entities and organizations), literary texts offer strikingly different distributions of entity categories, with much stronger emphasis on people and description of settings. We present empirical results demonstrating the performance of nested entity recognition models in this domain; training natively on in-domain literary data yields an improvement of over 20 absolute points in F-score (from 45.7 to 68.3), and mitigates a disparate impact in performance for male and female entities present in models trained on news data.",
}
```

### Event detection
```
@inproceedings{sims-etal-2019-literary,
    title = "Literary Event Detection",
    author = "Sims, Matthew  and
      Park, Jong Ho  and
      Bamman, David",
    editor = "Korhonen, Anna  and
      Traum, David  and
      M{\`a}rquez, Llu{\'\i}s",
    booktitle = "Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2019",
    address = "Florence, Italy",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/P19-1353",
    doi = "10.18653/v1/P19-1353",
    pages = "3623--3634",
    abstract = "In this work we present a new dataset of literary events{---}events that are depicted as taking place within the imagined space of a novel. While previous work has focused on event detection in the domain of contemporary news, literature poses a number of complications for existing systems, including complex narration, the depiction of a broad array of mental states, and a strong emphasis on figurative language. We outline the annotation decisions of this new dataset and compare several models for predicting events; the best performing model, a bidirectional LSTM with BERT token representations, achieves an F1 score of 73.9. We then apply this model to a corpus of novels split across two dimensions{---}prestige and popularity{---}and demonstrate that there are statistically significant differences in the distribution of events for prestige.",
}
```

### Coreference
```
@inproceedings{bamman-etal-2020-annotated,
    title = "An Annotated Dataset of Coreference in {E}nglish Literature",
    author = "Bamman, David  and
      Lewke, Olivia  and
      Mansoor, Anya",
    editor = "Calzolari, Nicoletta  and
      B{\'e}chet, Fr{\'e}d{\'e}ric  and
      Blache, Philippe  and
      Choukri, Khalid  and
      Cieri, Christopher  and
      Declerck, Thierry  and
      Goggi, Sara  and
      Isahara, Hitoshi  and
      Maegaard, Bente  and
      Mariani, Joseph  and
      Mazo, H{\'e}l{\`e}ne  and
      Moreno, Asuncion  and
      Odijk, Jan  and
      Piperidis, Stelios",
    booktitle = "Proceedings of the Twelfth Language Resources and Evaluation Conference",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://aclanthology.org/2020.lrec-1.6",
    pages = "44--54",
    abstract = "We present in this work a new dataset of coreference annotations for works of literature in English, covering 29,103 mentions in 210,532 tokens from 100 works of fiction published between 1719 and 1922. This dataset differs from previous coreference corpora in containing documents whose average length (2,105.3 words) is four times longer than other benchmark datasets (463.7 for OntoNotes), and contains examples of difficult coreference problems common in literature. This dataset allows for an evaluation of cross-domain performance for the task of coreference resolution, and analysis into the characteristics of long-distance within-document coreference.",
    language = "English",
    ISBN = "979-10-95546-34-4",
}
```