---
license: other
configs:
- config_name: ca_ancora-corefud
  data_files:
  - split: train
    path: ca_ancora-corefud/train-*
  - split: validation
    path: ca_ancora-corefud/validation-*
- config_name: cs_pcedt-corefud
  data_files:
  - split: train
    path: cs_pcedt-corefud/train-*
  - split: validation
    path: cs_pcedt-corefud/validation-*
- config_name: de_parcorfull-corefud
  data_files:
  - split: train
    path: de_parcorfull-corefud/train-*
  - split: validation
    path: de_parcorfull-corefud/validation-*
- config_name: de_potsdamcc-corefud
  data_files:
  - split: train
    path: de_potsdamcc-corefud/train-*
  - split: validation
    path: de_potsdamcc-corefud/validation-*
- config_name: en_gum-corefud
  data_files:
  - split: train
    path: en_gum-corefud/train-*
  - split: validation
    path: en_gum-corefud/validation-*
- config_name: en_parcorfull-corefud
  data_files:
  - split: train
    path: en_parcorfull-corefud/train-*
  - split: validation
    path: en_parcorfull-corefud/validation-*
- config_name: es_ancora-corefud
  data_files:
  - split: train
    path: es_ancora-corefud/train-*
  - split: validation
    path: es_ancora-corefud/validation-*
- config_name: hu_korkor-corefud
  data_files:
  - split: train
    path: hu_korkor-corefud/train-*
  - split: validation
    path: hu_korkor-corefud/validation-*
- config_name: hu_szegedkoref-corefud
  data_files:
  - split: train
    path: hu_szegedkoref-corefud/train-*
  - split: validation
    path: hu_szegedkoref-corefud/validation-*
- config_name: lt_lcc-corefud
  data_files:
  - split: train
    path: lt_lcc-corefud/train-*
  - split: validation
    path: lt_lcc-corefud/validation-*
- config_name: no_bokmaalnarc-corefud
  data_files:
  - split: train
    path: no_bokmaalnarc-corefud/train-*
  - split: validation
    path: no_bokmaalnarc-corefud/validation-*
- config_name: pl_pcc-corefud
  data_files:
  - split: train
    path: pl_pcc-corefud/train-*
  - split: validation
    path: pl_pcc-corefud/validation-*
- config_name: ru_rucor-corefud
  data_files:
  - split: train
    path: ru_rucor-corefud/train-*
  - split: validation
    path: ru_rucor-corefud/validation-*
- config_name: tr_itcc-corefud
  data_files:
  - split: train
    path: tr_itcc-corefud/train-*
  - split: validation
    path: tr_itcc-corefud/validation-*
- config_name: cs_pdt-corefud
  data_files:
  - split: train
    path: cs_pdt-corefud/train-*
  - split: validation
    path: cs_pdt-corefud/validation-*
- config_name: fr_democrat-corefud
  data_files:
  - split: train
    path: fr_democrat-corefud/train-*
  - split: validation
    path: fr_democrat-corefud/validation-*
- config_name: no_nynorsknarc-corefud
  data_files:
  - split: train
    path: no_nynorsknarc-corefud/train-*
  - split: validation
    path: no_nynorsknarc-corefud/validation-*
---

# CorefUD v1.1

- Project: https://ufal.mff.cuni.cz/corefud
- Data source: https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-5053

## Details

From https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-5053:

CorefUD is a collection of previously existing datasets annotated with coreference, which we converted into a common annotation scheme. In total, CorefUD in its current version 1.1 consists of 21 datasets for 13 languages. The datasets are enriched with automatic morphological and syntactic annotations that are fully compliant with the standards of the Universal Dependencies project. All the datasets are stored in the CoNLL-U format, with coreference- and bridging-specific information captured by attribute-value pairs located in the MISC column. The collection is divided into a public edition and a non-public (ÚFAL-internal) edition. The publicly available edition is distributed via LINDAT-CLARIAH-CZ and contains 17 datasets for 12 languages (1 dataset for Catalan, 2 for Czech, 2 for English, 1 for French, 2 for German, 2 for Hungarian, 1 for Lithuanian, 2 for Norwegian, 1 for Polish, 1 for Russian, 1 for Spanish, and 1 for Turkish), excluding the test data. The non-public edition is available internally to ÚFAL members and contains additional 4 datasets for 2 languages (1 dataset for Dutch, and 3 for English), which we are not allowed to distribute due to their original license limitations. It also contains the test data portions for all datasets. When using any of the harmonized datasets, please get acquainted with its license (placed in the same directory as the data) and cite the original data resource too. Compared to the previous version 1.0, the version 1.1 comprises new languages and corpora, namely Hungarian-KorKor, Norwegian-BokmaalNARC, Norwegian-NynorskNARC, and Turkish-ITCC. In addition, the English GUM dataset has been updated to a newer and larger version, and the conversion pipelines for most datasets have been refined (a list of all changes in each dataset can be found in the corresponding README file).

## Licenses

1. Catalan-AnCora: The treebank is licensed under the Creative Commons License Attribution 4.0 International. The complete license text is available at:
https://creativecommons.org/licenses/by/4.0/legalcode
1. Czech-PCEDT: Attribution-NonCommercial-ShareAlike 3.0 Unported
1. Czech-PDT: Attribution-NonCommercial-ShareAlike 4.0 International
1. GUM: Anootations are Creative Commons Attribution (CC-BY) version 4.0 Note: reddit data is excluded from CorefUD due to licensing:
    1. Wikinews/interviews:   http://creativecommons.org/licenses/by/2.5/ (Source: https://en.wikinews.org/wiki/Wikinews:Copyright)
    1. WikiVoyage: https://creativecommons.org/licenses/by-sa/3.0/ (Source: https://wikimediafoundation.org/wiki/Terms_of_Use)
    1. WikiHow:    http://creativecommons.org/licenses/by-nc-sa/3.0/ (Source: http://www.wikihow.com/wikiHow:Creative-Commons)
    1. Academic:  Multiple sources, all https://creativecommons.org/licenses/by/4.0/
    1. Biographies:   http://creativecommons.org/licenses/by-sa/3.0/ (Source: https://en.wikipedia.org/wiki/Wikipedia:Copyrights)
    1. Fiction:    http://creativecommons.org/licenses/by-nc-sa/3.0/ (Source: http://smallbeerpress.com/creative-commons/)
1. English-ParCorFull: Attribution-NonCommercial 4.0 International
1. French-Democrat: Attribution-ShareAlike 4.0 International
1. German-ParCorFull: Attribution-NonCommercial 4.0 International
1. German-PotsdamCC: Attribution-NonCommercial-ShareAlike 4.0 International
1. Hungarian-KorKor: Creative Commons Attribution 4.0 International Public License
1. Hungarian-SzegedKoref: Attribution 4.0 International
1. Lithuanian-LCC: CLARIN-LT PUBLIC END-USER LICENCE (PUB)
1. Norwegian-BokmaaINARC: Attribution-ShareAlike 4.0 International
1. Norwegian-NynorskNARC: Attribution-ShareAlike 4.0 International
1. Polish-PCC: CC Attribution 3.0 Unported
1. Russian-RuCor: Attribution-ShareAlike 4.0 International
1. Spanish-AnCora: Creative Commons License Attribution 4.0 International
1. Turkish-ITCC: Attribution-NonCommercial-ShareAlike 4.0 International

## Citation
```
 @misc{11234/1-5053,
 title = {Coreference in Universal Dependencies 1.1 ({CorefUD} 1.1)},
 author = {Nov{\'a}k, Michal and Popel, Martin and {\v Z}abokrtsk{\'y}, Zden{\v e}k and Zeman, Daniel and Nedoluzhko, Anna and Acar, Kutay and Bourgonje, Peter and Cinkov{\'a}, Silvie and Cebiro{\u g}lu Eryi{\u g}it, G{\"u}l{\c s}en and Haji{\v c}, Jan and Hardmeier, Christian and Haug, Dag and J{\o}rgensen, Tollef and K{\aa}sen, Andre and Krielke, Pauline and Landragin, Fr{\'e}d{\'e}ric and Lapshinova-Koltunski, Ekaterina and M{\ae}hlum, Petter and Mart{\'{\i}}, M. Ant{\`o}nia and Mikulov{\'a}, Marie and N{\o}klestad, Anders and Ogrodniczuk, Maciej and {\O}vrelid, Lilja and Pamay Arslan, Tu{\u g}ba and Recasens, Marta and Solberg, Per Erik and Stede, Manfred and Straka, Milan and Toldova, Svetlana and Vad{\'a}sz, No{\'e}mi and Velldal, Erik and Vincze, Veronika and Zeldes, Amir and {\v Z}itkus, Voldemaras},
 url = {http://hdl.handle.net/11234/1-5053},
 note = {{LINDAT}/{CLARIAH}-{CZ} digital library at the Institute of Formal and Applied Linguistics ({{\'U}FAL}), Faculty of Mathematics and Physics, Charles University},
 copyright = {Licence {CorefUD} v1.1},
 year = {2023} }
```

## Features
```python
{'coref_entities': [[{'eid': Value(dtype='string', id=None),
                      'eid_or_grp': Value(dtype='string', id=None),
                      'etype': Value(dtype='string', id=None),
                      'other': Value(dtype='string', id=None),
                      'sent_id': Value(dtype='string', id=None),
                      'span': Value(dtype='string', id=None)}]],
 'doc_id': Value(dtype='string', id=None),
 'sentences': [{'comment': Value(dtype='string', id=None),
                'global_entity': Value(dtype='string', id=None),
                'newdoc': Value(dtype='string', id=None),
                'newpar': Value(dtype='null', id=None),
                'sent_id': Value(dtype='string', id=None),
                'speaker': Value(dtype='null', id=None),
                'text': Value(dtype='string', id=None),
                'tokens': [{'coref_mentions': [{'eid': Value(dtype='string',
                                                             id=None),
                                                'eid_or_grp': Value(dtype='string',
                                                                    id=None),
                                                'etype': Value(dtype='string',
                                                               id=None),
                                                'other': Value(dtype='string',
                                                               id=None),
                                                'span': Value(dtype='string',
                                                              id=None)}],
                            'deprel': Value(dtype='string', id=None),
                            'feats': Value(dtype='string', id=None),
                            'form': Value(dtype='string', id=None),
                            'head': Value(dtype='int64', id=None),
                            'lemma': Value(dtype='string', id=None),
                            'misc': Value(dtype='string', id=None),
                            'ord': Value(dtype='float64', id=None),
                            'upos': Value(dtype='string', id=None),
                            'xpos': Value(dtype='string', id=None)}]}]}
```