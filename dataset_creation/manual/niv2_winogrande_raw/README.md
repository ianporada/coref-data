---
license: apache-2.0
---

# Natural Instructions v2 Winogrande Tasks

- Project: https://github.com/allenai/natural-instructions
- Data source: [DataProvenanceInitiative/niv2_submix_original](https://huggingface.co/datasets/DataProvenanceInitiative/niv2_submix_original)

## Details

This dataset contains all Winogrande examples that were included in the [Flan 2022 collection](https://github.com/google-research/FLAN/tree/main/flan/v2) which were orignally published in Super-Natural-Instructions.

The data is copied from the preprocessed Natural Instructions v2 dataset at [DataProvenanceInitiative/niv2_submix_original](https://huggingface.co/datasets/DataProvenanceInitiative/niv2_submix_original).

These tasks are:
1. 'task029_winogrande_full_object': Creating a pair of fill in the blank question-answer pairs on objects.	
2. 'task030_winogrande_full_person': Creating a pair of fill in the blank questions on persons.	
3. 'task031_winogrande_question_generation_object': Writing a fill in the blank question on objects.	
4. 'task032_winogrande_question_generation_person': Writing a fill in the blank question on persons.	
5. 'task033_winogrande_answer_generation': Answering a fill in the blank question on objects.	
6. 'task034_winogrande_question_modification_object': Modifying a fill in the blank question on objects.	
7. 'task035_winogrande_question_modification_person': Modifying a fill in the blank question on persons.	
8. 'task1391_winogrande_easy_answer_generation': Answering a fill in the blank question on objects.

### Fields

- `inputs`: a `string` feature.
- `targets`: a `string` feature.
- `task_source`: a `string` feature.
- `task_name`: a `string` feature.
- `template_type`: a `string` feature.

## Citation
```
@inproceedings{wang-etal-2022-super,
    title = "Super-{N}atural{I}nstructions: Generalization via Declarative Instructions on 1600+ {NLP} Tasks",
    author = "Wang, Yizhong  and
      Mishra, Swaroop  and
      Alipoormolabashi, Pegah  and
      Kordi, Yeganeh  and
      Mirzaei, Amirreza  and
      Naik, Atharva  and
      Ashok, Arjun  and
      Dhanasekaran, Arut Selvan  and
      Arunkumar, Anjana  and
      Stap, David  and
      Pathak, Eshaan  and
      Karamanolakis, Giannis  and
      Lai, Haizhi  and
      Purohit, Ishan  and
      Mondal, Ishani  and
      Anderson, Jacob  and
      Kuznia, Kirby  and
      Doshi, Krima  and
      Pal, Kuntal Kumar  and
      Patel, Maitreya  and
      Moradshahi, Mehrad  and
      Parmar, Mihir  and
      Purohit, Mirali  and
      Varshney, Neeraj  and
      Kaza, Phani Rohitha  and
      Verma, Pulkit  and
      Puri, Ravsehaj Singh  and
      Karia, Rushang  and
      Doshi, Savan  and
      Sampat, Shailaja Keyur  and
      Mishra, Siddhartha  and
      Reddy A, Sujan  and
      Patro, Sumanta  and
      Dixit, Tanay  and
      Shen, Xudong",
    editor = "Goldberg, Yoav  and
      Kozareva, Zornitsa  and
      Zhang, Yue",
    booktitle = "Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing",
    month = dec,
    year = "2022",
    address = "Abu Dhabi, United Arab Emirates",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2022.emnlp-main.340",
    doi = "10.18653/v1/2022.emnlp-main.340",
    pages = "5085--5109",
    abstract = "How well can NLP models generalize to a variety of unseen tasks when provided with task instructions? To address this question, we first introduce Super-NaturalInstructions, a benchmark of 1,616 diverse NLP tasks and their expert-written instructions. Our collection covers 76 distinct task types, including but not limited to classification, extraction, infilling, sequence tagging, text rewriting, and text composition. This large and diverse collection of tasks enables rigorous benchmarking of cross-task generalization under instructions{---}training models to follow instructions on a subset of tasks and evaluating them on the remaining unseen ones. Furthermore, we build Tk-Instruct, a transformer model trained to follow a variety of in-context instructions (plain language task definitions or k-shot examples). Our experiments show that Tk-Instruct outperforms existing instruction-following models such as InstructGPT by over 9{\%} on our benchmark despite being an order of magnitude smaller. We further analyze generalization as a function of various scaling parameters, such as the number of observed tasks, the number of instances per task, and model sizes. We hope our dataset and model facilitate future progress towards more general-purpose NLP models.",
}
```