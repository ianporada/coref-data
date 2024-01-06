---
language:
- en
paperswithcode_id: winogrande
pretty_name: WinoGrande
dataset_info:
- config_name: winogrande_xs
  features:
  - name: sentence
    dtype: string
  - name: option1
    dtype: string
  - name: option2
    dtype: string
  - name: answer
    dtype: string
  splits:
  - name: train
    num_bytes: 20704
    num_examples: 160
  - name: test
    num_bytes: 227649
    num_examples: 1767
  - name: validation
    num_bytes: 164199
    num_examples: 1267
  download_size: 3395492
  dataset_size: 412552
- config_name: winogrande_s
  features:
  - name: sentence
    dtype: string
  - name: option1
    dtype: string
  - name: option2
    dtype: string
  - name: answer
    dtype: string
  splits:
  - name: train
    num_bytes: 82308
    num_examples: 640
  - name: test
    num_bytes: 227649
    num_examples: 1767
  - name: validation
    num_bytes: 164199
    num_examples: 1267
  download_size: 3395492
  dataset_size: 474156
- config_name: winogrande_m
  features:
  - name: sentence
    dtype: string
  - name: option1
    dtype: string
  - name: option2
    dtype: string
  - name: answer
    dtype: string
  splits:
  - name: train
    num_bytes: 329001
    num_examples: 2558
  - name: test
    num_bytes: 227649
    num_examples: 1767
  - name: validation
    num_bytes: 164199
    num_examples: 1267
  download_size: 3395492
  dataset_size: 720849
- config_name: winogrande_l
  features:
  - name: sentence
    dtype: string
  - name: option1
    dtype: string
  - name: option2
    dtype: string
  - name: answer
    dtype: string
  splits:
  - name: train
    num_bytes: 1319576
    num_examples: 10234
  - name: test
    num_bytes: 227649
    num_examples: 1767
  - name: validation
    num_bytes: 164199
    num_examples: 1267
  download_size: 3395492
  dataset_size: 1711424
- config_name: winogrande_xl
  features:
  - name: sentence
    dtype: string
  - name: option1
    dtype: string
  - name: option2
    dtype: string
  - name: answer
    dtype: string
  splits:
  - name: train
    num_bytes: 5185832
    num_examples: 40398
  - name: test
    num_bytes: 227649
    num_examples: 1767
  - name: validation
    num_bytes: 164199
    num_examples: 1267
  download_size: 3395492
  dataset_size: 5577680
- config_name: winogrande_debiased
  features:
  - name: sentence
    dtype: string
  - name: option1
    dtype: string
  - name: option2
    dtype: string
  - name: answer
    dtype: string
  splits:
  - name: train
    num_bytes: 1203420
    num_examples: 9248
  - name: test
    num_bytes: 227649
    num_examples: 1767
  - name: validation
    num_bytes: 164199
    num_examples: 1267
  download_size: 3395492
  dataset_size: 1595268
license: cc-by-4.0
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