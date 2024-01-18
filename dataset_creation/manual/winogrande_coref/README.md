---
license: cc-by-4.0
---

# Wingrande Recast as Coreference Resolution

### Dataset Summary

WinoGrande train and development sets recast as coreference resolution as described in [Investigating Failures to Generalize for Coreference Resolution Models](https://arxiv.org/abs/2303.09092). Conllu columns are parsed using Stanza.

### Data Fields

```python
{
  "id": str, # example id
  "text": str, # untokenized example text
  "sentences": [
    {
      "id": int, # sentence index
      "text": str, # untokenized sentence text
      "speaker": None, # speaker
      "tokens": [
        {
          # keys are conllu columns: id, text, lemma, upos, xpos, feats, head, deprel, deps, misc
        },
        ...
      ]
    },
    ...
  ],
  "coref_chains": List[List[List[int]]], # list of clusters, each cluster is a list of mentions, each mention is a span represented as [sent, start, end] inclusive
  "genre": "crowdsourced",
  "meta_data": {
      "comment": "syntax_annotations=stanza|tokenizer=stanza|detokenizer=nltk",
  },
}
```

### Citation Information

```
@misc{porada2023investigating,
    title={Investigating Failures to Generalize for Coreference Resolution Models},
    author={Ian Porada and Alexandra Olteanu and Kaheer Suleman and Adam Trischler and Jackie Chi Kit Cheung},
    year={2023},
    eprint={2303.09092},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}

@InProceedings{ai2:winogrande,
  title = {WinoGrande: An Adversarial Winograd Schema Challenge at Scale},
  authors={Keisuke, Sakaguchi and Ronan, Le Bras and Chandra, Bhagavatula and Yejin, Choi
  },
  year={2019}
}
```
