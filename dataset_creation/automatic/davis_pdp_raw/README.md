---
license: cc-by-4.0
---

# Pronoun Disambiguation Problems (PDP) from the 2016 WSC as hosted by Ernest Davis


60 pronoun disambiguation problems from https://cs.nyu.edu/faculty/davise/papers/WinogradSchemas/WS.html

### Data Fields

- `text` (str): The text sequence
- `options` (list[str]): The two entity options that the pronoun may be referring to
- `label` (int): The index of the correct option in the `options` field
- `pronoun` (str): The pronoun in the sequence to be resolved
- `pronoun_loc` (int): The starting position of the pronoun in the sequence
- `quote` (str): The substr with the key action or context surrounding the pronoun
- `quote_loc` (int): The starting position of the quote in the sequence
- `source` (str): A description of the source who contributed the example

```
@article{Davis_Morgenstern_Ortiz_2017,
	title        = {The First Winograd Schema Challenge at IJCAI-16},
	author       = {Davis, Ernest and Morgenstern, Leora and Ortiz, Charles L.},
	year         = 2017,
	month        = {Oct.},
	journal      = {AI Magazine},
	volume       = 38,
	number       = 3,
	pages        = {97--98},
	doi          = {10.1609/aimag.v38i4.2734},
	url          = {https://ojs.aaai.org/aimagazine/index.php/aimagazine/article/view/2734},
	abstractnote = {The first Winograd Schema Challenge was held in New York, New York, as part of the International Joint Conference on Artificial Intelligence. The challenge was original conceived by Hector Levesque as an alternative to the Turing Test. This report details the results of this first challenge.}
}
```