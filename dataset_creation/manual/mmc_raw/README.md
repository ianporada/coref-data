---
license: apache-2.0
---

# MMC (Multilingual Multiparty Coreference)

- Project: https://github.com/boyuanzheng010/mmc
- Data source: https://github.com/boyuanzheng010/mmc/commit/a7007d1d4556a3f4347a3d7b686f71d66bd1e2d9

## Details

Data for the paper "Multilingual Coreference Resolution in Multiparty Dialogue" TACL 2023

## Citation
```
@article{zheng-etal-2023-multilingual,
    title = "Multilingual Coreference Resolution in Multiparty Dialogue",
    author = "Zheng, Boyuan  and
      Xia, Patrick  and
      Yarmohammadi, Mahsa  and
      Van Durme, Benjamin",
    journal = "Transactions of the Association for Computational Linguistics",
    volume = "11",
    year = "2023",
    address = "Cambridge, MA",
    publisher = "MIT Press",
    url = "https://aclanthology.org/2023.tacl-1.52",
    doi = "10.1162/tacl_a_00581",
    pages = "922--940",
    abstract = "Existing multiparty dialogue datasets for entity coreference resolution are nascent, and many challenges are still unaddressed. We create a large-scale dataset, Multilingual Multiparty Coref (MMC), for this task based on TV transcripts. Due to the availability of gold-quality subtitles in multiple languages, we propose reusing the annotations to create silver coreference resolution data in other languages (Chinese and Farsi) via annotation projection. On the gold (English) data, off-the-shelf models perform relatively poorly on MMC, suggesting that MMC has broader coverage of multiparty coreference than prior datasets. On the silver data, we find success both using it for data augmentation and training from scratch, which effectively simulates the zero-shot cross-lingual setting.",
}
```