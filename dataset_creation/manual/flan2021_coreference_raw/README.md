---
license: other
---

# Flan 2021 Coreference Tasks

- Project: https://github.com/google-research/FLAN/tree/main/flan/v2
- Data source: [DataProvenanceInitiative/flan2021_submix_original](https://huggingface.co/datasets/DataProvenanceInitiative/flan2021_submix_original)

## Details

This dataset contains all coreference examples that were included in the [Flan 2022 collection](https://github.com/google-research/FLAN/tree/main/flan/v2) which were orignally included in Flan 2021.

The data is copied from the preprocessed Flan2021 dataset at [DataProvenanceInitiative/flan2021_submix_original](https://huggingface.co/datasets/DataProvenanceInitiative/flan2021_submix_original).

```python
COREFERENCE_TASK_NAMES = {
    'definite_pronoun_resolution:1.1.0',
    'glue/wnli:2.0.0',
    'super_glue/wsc.fixed:1.0.2',
    'winogrande:1.1.0',
}
```

This does not include tasks that are tangentially coreference, e.g. "quoref" tasks in "DataProvenanceInitiative/t0_submix_original" and "qrecc" tasks in "DataProvenanceInitiative/dialog_submix_original".

### Fields

- `inputs`: a `string` feature.
- `targets`: a `string` feature.
- `task_source`: a `string` feature.
- `task_name`: a `string` feature.
- `template_type`: a `string` feature.

## Citation
```
@inproceedings{flan_2022_collection,
    author = {Longpre, Shayne and Hou, Le and Vu, Tu and Webson, Albert and Chung, Hyung Won and Tay, Yi and Zhou, Denny and Le, Quoc V. and Zoph, Barret and Wei, Jason and Roberts, Adam},
    title = {The flan collection: designing data and methods for effective instruction tuning},
    year = {2023},
    publisher = {JMLR.org},
    abstract = {We study the design decisions of publicly available instruction tuning methods, by reproducing and breaking down the development of Flan 2022 (Chung et al., 2022). Through careful ablation studies on the Flan Collection of tasks and methods, we tease apart the effect of design decisions which enable Flan-T5 to outperform prior work by 3-17\%+ across evaluation settings. We find task balancing and enrichment techniques are overlooked but critical to effective instruction tuning, and in particular, training with mixed prompt settings (zero-shot, few-shot, chain-of-thought) actually yields equivalent or stronger (2\%+) performance in all settings. In further experiments, we show Flan-T5 requires less finetuning to converge higher and faster than T5 on single downstream tasks--motivating instruction-tuned models as more computationally-efficient starting checkpoints for new tasks. Finally, to accelerate research on instruction tuning, we make the Flan 2022 collection of datasets, templates, and methods publicly available.},
    booktitle = {Proceedings of the 40th International Conference on Machine Learning},
    articleno = {941},
    numpages = {18},
    location = {Honolulu, Hawaii, USA},
    series = {ICML'23}
}
```