---
license: unknown
configs:
- config_name: wsc.fixed
  data_files:
  - split: train
    path: "wsc.fixed/train-*.parquet"
  - split: validation
    path: "wsc.fixed/validation-*.parquet"
  - split: test
    path: "wsc.fixed/test-*.parquet"
- config_name: wsc
  data_files:
  - split: train
    path: "wsc/train-*.parquet"
  - split: validation
    path: "wsc/validation-*.parquet"
  - split: test
    path: "wsc/test-*.parquet"
---

# Winograd Schema Challenge examples included in the SuperGLUE Benchmark

Specifically: The wsc and wsc.fixed datasets from the HuggingFace "super_glue" repository.

### Data Fields

- **`text`** (*`str`*): The text of the schema.
- **`span1_index`** (*`int`*): Starting word index of first entity.
- **`span2_index`** (*`int`*): Starting word index of second entity.
- **`span1_text`** (*`str`*): Textual representation of first entity.
- **`span2_text`** (*`str`*): Textual representation of second entity.
- **`idx`** (*`int`*): Index of the example in the dataset.
- **`label`** (*`bool`*): True if the two spans corefer.

"""The primary SuperGLUE tasks are built on and derived from existing datasets. We refer users to the original licenses accompanying each dataset, but it is our understanding that these licenses allow for their use and redistribution in a research context."""

```
@inproceedings{NEURIPS2019_4496bf24,
 author = {Wang, Alex and Pruksachatkun, Yada and Nangia, Nikita and Singh, Amanpreet and Michael, Julian and Hill, Felix and Levy, Omer and Bowman, Samuel},
 booktitle = {Advances in Neural Information Processing Systems},
 editor = {H. Wallach and H. Larochelle and A. Beygelzimer and F. d\textquotesingle Alch\'{e}-Buc and E. Fox and R. Garnett},
 pages = {},
 publisher = {Curran Associates, Inc.},
 title = {SuperGLUE: A Stickier Benchmark for General-Purpose Language Understanding Systems},
 url = {https://proceedings.neurips.cc/paper_files/paper/2019/file/4496bf24afe7fab6f046bf4923da8de6-Paper.pdf},
 volume = {32},
 year = {2019}
}
```

### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@lewtun](https://github.com/lewtun), [@patrickvonplaten](https://github.com/patrickvonplaten) for adding this dataset.