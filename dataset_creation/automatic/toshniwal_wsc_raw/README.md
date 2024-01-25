---
license: cc-by-nd-4.0
---

# gen_winograd

- Project: https://github.com/shtoshni/fast-coref
- Data source: https://github.com/shtoshni/fast-coref/blob/527e3a1c73719ae7443945f12237bcd97b84572f/src/data_processing/process_wsc.py

## Details

The original WSC manually reformatted with annotated mentions.

## Citation
```
@inproceedings{toshniwal-etal-2021-generalization,
    title = "On Generalization in Coreference Resolution",
    author = "Toshniwal, Shubham  and
      Xia, Patrick  and
      Wiseman, Sam  and
      Livescu, Karen  and
      Gimpel, Kevin",
    editor = "Ogrodniczuk, Maciej  and
      Pradhan, Sameer  and
      Poesio, Massimo  and
      Grishina, Yulia  and
      Ng, Vincent",
    booktitle = "Proceedings of the Fourth Workshop on Computational Models of Reference, Anaphora and Coreference",
    month = nov,
    year = "2021",
    address = "Punta Cana, Dominican Republic",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.crac-1.12",
    doi = "10.18653/v1/2021.crac-1.12",
    pages = "111--120",
    abstract = "While coreference resolution is defined independently of dataset domain, most models for performing coreference resolution do not transfer well to unseen domains. We consolidate a set of 8 coreference resolution datasets targeting different domains to evaluate the off-the-shelf performance of models. We then mix three datasets for training; even though their domain, annotation guidelines, and metadata differ, we propose a method for jointly training a single model on this heterogeneous data mixture by using data augmentation to account for annotation differences and sampling to balance the data quantities. We find that in a zero-shot setting, models trained on a single dataset transfer poorly while joint training yields improved overall performance, leading to better generalization in coreference resolution models. This work contributes a new benchmark for robust coreference resolution and multiple new state-of-the-art results.",
}
```