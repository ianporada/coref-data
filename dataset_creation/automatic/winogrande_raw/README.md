---
license: cc-by-4.0
configs:
- config_name: winogrande_debiased
  data_files:
  - split: train
    path: "winogrande_debiased/train-*.parquet"
  - split: validation
    path: "winogrande_debiased/validation-*.parquet"
  - split: test
    path: "winogrande_debiased/test-*.parquet"
- config_name: winogrande_l
  data_files:
  - split: train
    path: "winogrande_l/train-*.parquet"
  - split: validation
    path: "winogrande_l/validation-*.parquet"
  - split: test
    path: "winogrande_l/test-*.parquet"
- config_name: winogrande_m
  data_files:
  - split: train
    path: "winogrande_m/train-*.parquet"
  - split: validation
    path: "winogrande_m/validation-*.parquet"
  - split: test
    path: "winogrande_m/test-*.parquet"
- config_name: winogrande_s
  data_files:
  - split: train
    path: "winogrande_s/train-*.parquet"
  - split: validation
    path: "winogrande_s/validation-*.parquet"
  - split: test
    path: "winogrande_s/test-*.parquet"
- config_name: winogrande_xl
  data_files:
  - split: train
    path: "winogrande_xl/train-*.parquet"
  - split: validation
    path: "winogrande_xl/validation-*.parquet"
  - split: test
    path: "winogrande_xl/test-*.parquet"
- config_name: winogrande_xs
  data_files:
  - split: train
    path: "winogrande_xs/train-*.parquet"
  - split: validation
    path: "winogrande_xs/validation-*.parquet"
  - split: test
    path: "winogrande_xs/test-*.parquet"
---

# Wingrande v1.1

## Dataset Description

- **Homepage:** [https://leaderboard.allenai.org/winogrande/submissions/get-started](https://leaderboard.allenai.org/winogrande/submissions/get-started)
- **Size of downloaded dataset files:** 20.37 MB
- **Size of the generated dataset:** 10.50 MB
- **Total amount of disk used:** 30.87 MB

### Dataset Summary

WinoGrande is a new collection of 44k problems, inspired by Winograd Schema Challenge (Levesque, Davis, and Morgenstern
 2011), but adjusted to improve the scale and robustness against the dataset-specific bias. Formulated as a
fill-in-a-blank task with binary options, the goal is to choose the right option for a given sentence which requires
commonsense reasoning.

### Data Fields

The data fields are the same among all splits.

- `sentence`: a `string` feature.
- `option1`: a `string` feature.
- `option2`: a `string` feature.
- `answer`: a `string` feature.

### Data Splits

|       name        |train|validation|test|
|-------------------|----:|---------:|---:|
|winogrande_debiased| 9248|      1267|1767|
|winogrande_l       |10234|      1267|1767|
|winogrande_m       | 2558|      1267|1767|
|winogrande_s       |  640|      1267|1767|
|winogrande_xl      |40398|      1267|1767|
|winogrande_xs      |  160|      1267|1767|

### Citation Information

```
@InProceedings{ai2:winogrande,
  title = {WinoGrande: An Adversarial Winograd Schema Challenge at Scale},
  authors={Keisuke, Sakaguchi and Ronan, Le Bras and Chandra, Bhagavatula and Yejin, Choi
  },
  year={2019}
}

```

### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@TevenLeScao](https://github.com/TevenLeScao), [@patrickvonplaten](https://github.com/patrickvonplaten), [@lewtun](https://github.com/lewtun) for adding this dataset.