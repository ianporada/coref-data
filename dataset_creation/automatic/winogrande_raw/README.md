---
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