---
license: other
---

# ARRAU Version 2.1

- Project: https://sites.google.com/view/arrau/corpus
- Data source: https://catalog.ldc.upenn.edu/LDC2013T22 (Private distribution)

## Details

Sub-corpora (original split):
1. Gnome (no split)
1. Pear Stories (no split)
1. RST DTreeBank (train, dev, test)
1. Trains 91 (no split)
1. Trains 93 (no split)
1. VPC (train, test) <- VPC is a subset of RST

### Classes

#### Coref

* ambiguity \in {None, 'ambiguous_antecedent', 'ambiguous', 'unambiguous'}
* gender \in {'unspecified', 'neut', 'female', 'male', 'neuter', 'fem', 'masc', 'unmarked', 'undersp-gen'}
* non_ref_type \in {None, 'coordination', 'expletive', 'quantifier', 'incomplete', 'unknown', 'predicate', 'idiom'}
* non_ref_type_2 \in {None, 'unknown', 'expletive'}
* number \in {'sing', 'mass', 'plur', 'unmarked', 'undersp-num', 'unsure-num'}
* person \in {'per2', 'per3', 'per1'}
* ref_type \in {None, 'phrase', 'segment'}
* ref_type_2 \in {None, 'non_referring', 'new', 'segment', 'phrase'}
* reference \in {'old', 'non_referring', 'new', 'undef_reference', 'unmarked'}
* generic_2 \in {None, 'generic-yes', 'generic-no', 'undersp-replicable'}

if reg_type == segment, segment_antecedent indicates discourse deixis phrase unit, but the phrase unit is not a mention

related_phrase:mention_id and related_rel mark bridging anaphora

#### Markable
* isprenominal \in {'true', 'false'}
* label \in {'person', 'organization', 'np', 'location'}

#### Statistics
Total markables: 99582 \
Split and no min: 1057 \
Crossing sentence boundary: 355 \
No entity set: 5

## Citation
```
@article{uryupina_artstein_bristot_cavicchio_delogu_rodriguez_poesio_2020,
    title={Annotating a broad range of anaphoric phenomena, in a variety of genres: the ARRAU Corpus},
    volume={26}, DOI={10.1017/S1351324919000056},
    number={1},
    journal={Natural Language Engineering},
    publisher={Cambridge University Press},
    author={Uryupina, Olga and Artstein, Ron and Bristot, Antonella and Cavicchio, Federica and Delogu, Francesca and Rodriguez, Kepa J. and Poesio, Massimo},
    year={2020},
    pages={95–128}
}
```

## Features

```python
{'chunk': [{'id': Value(dtype='string', id=None),
            'mmax_level': Value(dtype='string', id=None),
            'span': Value(dtype='string', id=None),
            'tag': Value(dtype='string', id=None)}],
 'coref': [{'ambiguity': Value(dtype='string', id=None),
            'category': Value(dtype='string', id=None),
            'category_2': Value(dtype='string', id=None),
            'comment': Value(dtype='string', id=None),
            'coref_set': Value(dtype='string', id=None),
            'gender': Value(dtype='string', id=None),
            'generic': Value(dtype='string', id=None),
            'generic_2': Value(dtype='string', id=None),
            'gram_fnc': Value(dtype='string', id=None),
            'id': Value(dtype='string', id=None),
            'min_ids': Value(dtype='string', id=None),
            'min_words': Value(dtype='string', id=None),
            'mmax_level': Value(dtype='string', id=None),
            'multiple_phrase_antecedents': Value(dtype='string', id=None),
            'multiple_phrase_antecedents_2': Value(dtype='string', id=None),
            'non_ref_type': Value(dtype='string', id=None),
            'non_ref_type_2': Value(dtype='string', id=None),
            'number': Value(dtype='string', id=None),
            'object': Value(dtype='string', id=None),
            'object_2': Value(dtype='string', id=None),
            'on_map': Value(dtype='string', id=None),
            'on_map_2': Value(dtype='string', id=None),
            'person': Value(dtype='string', id=None),
            'phrase_antecedent': Value(dtype='string', id=None),
            'phrase_antecedent_2': Value(dtype='string', id=None),
            'ref_type': Value(dtype='string', id=None),
            'ref_type_2': Value(dtype='string', id=None),
            'reference': Value(dtype='string', id=None),
            'related_object': Value(dtype='string', id=None),
            'related_object_2': Value(dtype='string', id=None),
            'related_phrase': Value(dtype='string', id=None),
            'related_phrase_2': Value(dtype='string', id=None),
            'related_rel': Value(dtype='string', id=None),
            'related_rel_2': Value(dtype='string', id=None),
            'segment_antecedent': Value(dtype='string', id=None),
            'segment_antecedent_2': Value(dtype='string', id=None),
            'single_phrase_antecedent': Value(dtype='string', id=None),
            'single_phrase_antecedent_2': Value(dtype='string', id=None),
            'span': Value(dtype='string', id=None),
            'type': Value(dtype='string', id=None)}],
 'corpus': Value(dtype='string', id=None),
 'document_name': Value(dtype='string', id=None),
 'enamex': [{'id': Value(dtype='string', id=None),
             'mmax_level': Value(dtype='string', id=None),
             'span': Value(dtype='string', id=None),
             'tag': Value(dtype='string', id=None)}],
 'markable': [{'id': Value(dtype='string', id=None),
               'isprenominal': Value(dtype='string', id=None),
               'label': Value(dtype='string', id=None),
               'lemmata': Value(dtype='string', id=None),
               'min_ids': Value(dtype='string', id=None),
               'mmax_level': Value(dtype='string', id=None),
               'pos': Value(dtype='string', id=None),
               'sentenceid': Value(dtype='string', id=None),
               'span': Value(dtype='string', id=None),
               'type': Value(dtype='string', id=None)}],
 'morph': [{'id': Value(dtype='string', id=None),
            'lemma': Value(dtype='string', id=None),
            'mmax_level': Value(dtype='string', id=None),
            'span': Value(dtype='string', id=None)}],
 'parse': [{'id': Value(dtype='string', id=None),
            'mmax_level': Value(dtype='string', id=None),
            'span': Value(dtype='string', id=None),
            'tag': Value(dtype='string', id=None)}],
 'phrase': [{'ambiguity': Value(dtype='string', id=None),
             'category': Value(dtype='string', id=None),
             'category_2': Value(dtype='string', id=None),
             'comment': Value(dtype='string', id=None),
             'gender': Value(dtype='string', id=None),
             'generic': Value(dtype='string', id=None),
             'generic_2': Value(dtype='string', id=None),
             'gram_fnc': Value(dtype='string', id=None),
             'id': Value(dtype='string', id=None),
             'min_ids': Value(dtype='string', id=None),
             'min_words': Value(dtype='string', id=None),
             'mmax_level': Value(dtype='string', id=None),
             'multiple_phrase_antecedents': Value(dtype='string', id=None),
             'multiple_phrase_antecedents_2': Value(dtype='string', id=None),
             'non_ref_type': Value(dtype='string', id=None),
             'non_ref_type_2': Value(dtype='string', id=None),
             'number': Value(dtype='string', id=None),
             'object': Value(dtype='string', id=None),
             'object_2': Value(dtype='string', id=None),
             'on_map': Value(dtype='string', id=None),
             'on_map_2': Value(dtype='string', id=None),
             'person': Value(dtype='string', id=None),
             'phrase_antecedent': Value(dtype='string', id=None),
             'phrase_antecedent_2': Value(dtype='string', id=None),
             'ref_type': Value(dtype='string', id=None),
             'ref_type_2': Value(dtype='string', id=None),
             'reference': Value(dtype='string', id=None),
             'related_object': Value(dtype='string', id=None),
             'related_object_2': Value(dtype='string', id=None),
             'related_phrase': Value(dtype='string', id=None),
             'related_phrase_2': Value(dtype='string', id=None),
             'related_rel': Value(dtype='string', id=None),
             'related_rel_2': Value(dtype='string', id=None),
             'segment_antecedent': Value(dtype='string', id=None),
             'segment_antecedent_2': Value(dtype='string', id=None),
             'single_phrase_antecedent': Value(dtype='string', id=None),
             'single_phrase_antecedent_2': Value(dtype='string', id=None),
             'span': Value(dtype='string', id=None),
             'type': Value(dtype='string', id=None)}],
 'pos': [{'id': Value(dtype='string', id=None),
          'mmax_level': Value(dtype='string', id=None),
          'span': Value(dtype='string', id=None),
          'tag': Value(dtype='string', id=None)}],
 'sentence': [{'id': Value(dtype='string', id=None),
               'mmax_level': Value(dtype='string', id=None),
               'orderid': Value(dtype='string', id=None),
               'span': Value(dtype='string', id=None)}],
 'split': Value(dtype='string', id=None),
 'unit': [{'finite': Value(dtype='string', id=None),
           'id': Value(dtype='string', id=None),
           'mmax_level': Value(dtype='string', id=None),
           'span': Value(dtype='string', id=None),
           'subject': Value(dtype='string', id=None),
           'utype': Value(dtype='string', id=None),
           'verbed': Value(dtype='string', id=None)}],
 'utterance': [{'id': Value(dtype='string', id=None),
                'mmax_level': Value(dtype='string', id=None),
                'span': Value(dtype='string', id=None),
                'type': Value(dtype='string', id=None)}],
 'words': [{'id': Value(dtype='string', id=None),
            'text': Value(dtype='string', id=None)}]}
```
