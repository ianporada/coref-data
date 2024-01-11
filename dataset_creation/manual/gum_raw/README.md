---
license: other
---

# GUM Corpus

- Project: https://github.com/amir-zeldes/gum
- Data source: https://github.com/amir-zeldes/gum/commit/3b0ab7d11911be1695e4dacadb28a7a1df230bdb (V9.2.0)

## Details

An English corpus annotated for coreference and other linguistic phenomenon. See the project repo for full corpora license information. Annotations are licensed under CC-BY-4.0.

## Citation
```
@Article{Zeldes2017,
  author    = {Amir Zeldes},
  title     = {The {GUM} Corpus: Creating Multilayer Resources in the Classroom},
  journal   = {Language Resources and Evaluation},
  year      = {2017},
  volume    = {51},
  number    = {3},
  pages     = {581--612},
  doi       = {http://dx.doi.org/10.1007/s10579-016-9343-x}
}

@InProceedings{ZhuEtAl2021,
  author    = {Yilun Zhu and Sameer Pradhan and Amir Zeldes},
  booktitle = {Proceedings of ACL-IJCNLP 2021},
  title     = {{OntoGUM}: Evaluating Contextualized {SOTA} Coreference Resolution on 12 More Genres},
  year      = {2021},
  pages     = {461--467},
  address   = {Bangkok, Thailand}
}
```

## Features

```python
{
    "doc_id": Value(dtype="string", id=None),
    "sentences": [
        {
            "comment": Value(dtype="string", id=None),
            "conll_rows": [
                {
                    "deprel": Value(dtype="string", id=None),
                    "deps": Value(dtype="string", id=None),
                    "feats": Value(dtype="string", id=None),
                    "head": Value(dtype="int64", id=None),
                    "id": Value(dtype="int64", id=None),
                    "lemma": Value(dtype="string", id=None),
                    "misc": Value(dtype="string", id=None),
                    "text": Value(dtype="string", id=None),
                    "upos": Value(dtype="string", id=None),
                    "xpos": Value(dtype="string", id=None),
                }
            ],
            "global_entity": Value(dtype="string", id=None),
            "newdoc": Value(dtype="string", id=None),
            "newpar": Value(dtype="bool", id=None),
            "sent_id": Value(dtype="string", id=None),
            "speaker": Value(dtype="string", id=None),
            "text": Value(dtype="string", id=None),
            "tokens": [
                {
                    "coref_mentions": [
                        {
                            "eid": Value(dtype="string", id=None),
                            "eid_or_grp": Value(dtype="string", id=None),
                            "etype": Value(dtype="string", id=None),
                            "other": {
                                "centering": Value(dtype="string", id=None),
                                "identity": Value(dtype="string", id=None),
                                "infstat": Value(dtype="string", id=None),
                                "link": Value(dtype="string", id=None),
                                "minspan": Value(dtype="string", id=None),
                            },
                            "span": Value(dtype="string", id=None),
                        }
                    ],
                    "deprel": Value(dtype="string", id=None),
                    "form": Value(dtype="string", id=None),
                    "head": Value(dtype="int64", id=None),
                    "lemma": Value(dtype="string", id=None),
                    "ord": Value(dtype="float64", id=None),
                    "upos": Value(dtype="string", id=None),
                    "xpos": Value(dtype="string", id=None),
                }
            ],
        }
    ],
    "ontogum_sentences": [
        [
            {
                "deprel": Value(dtype="string", id=None),
                "deps": Value(dtype="string", id=None),
                "feats": Value(dtype="string", id=None),
                "head": Value(dtype="int64", id=None),
                "id": Value(dtype="int64", id=None),
                "lemma": Value(dtype="string", id=None),
                "misc": Value(dtype="string", id=None),
                "text": Value(dtype="string", id=None),
                "upos": Value(dtype="string", id=None),
                "xpos": Value(dtype="string", id=None),
            }
        ]
    ],
    "ontogum_coref_chains": Sequence(
        feature=Sequence(
            feature=Sequence(feature=Value(dtype="int64", id=None), length=-1, id=None),
            length=-1,
            id=None,
        ),
        length=-1,
        id=None,
    ),
}
```