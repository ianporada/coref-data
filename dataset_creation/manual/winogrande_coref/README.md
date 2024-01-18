---
license: cc-by-4.0
---

# Wingrande Recast as Coreference Resolution

### Dataset Summary

WinoGrande train and development sets recast as coreference resolution as described in [Investigating Failures to Generalize for Coreference Resolution Models](https://arxiv.org/abs/2303.09092). Conllu columns are parsed using Stanza.

### Data Fields

```python
{
    "doc_name": doc_name, # document name
    "sentences": sentences, # list of sentences, each sentence is a list of conllu lines
    "coref_chains": coref_chains, # list of clusters, each cluster is a list of mentions of form [sent, start, end] inclusive
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
