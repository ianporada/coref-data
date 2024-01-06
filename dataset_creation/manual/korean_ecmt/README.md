
# Korean Effective Crowdsourcing of Multiple Tasks (ECMT) for Comprehensive Knowledge Extraction

## Details

Annotated text from Korean Wikipedia and DBox (DBpedia).

The dataset was annotated by crowdworks in multiple stages.
* Phase I: entity mention detection annotation; candidate entity mentions are selected in a text
* Phase II: entity linking annotation; candidate mentions can be linked to a knowledge base
* Phase III: coreference annotation; entities can be linked to pronouns, demonstrative determiners, and antecedent mentions
* Phase IV: relation extraction annotation; relations between entities are annotated

### Annotation Notes

#### Phase I
* For each mention, the annotator selects a category from one of 16 options: person, study field, theory, artifact, organization, location, civilization, event, year, time, quantity, job, animal, plant, material, and term.
* Entities can be things, concepts, ideas, or events:
```
개체란 다른 것들과 분리되어 존재하는 것으로, 개체는 물질적 존재일 필요는 없으며 개념적 아이디어 혹은 사건도 될 수 있다 개체의 대표적인 범주에는 사람, 물체, 조직, 기관, 장소, 시간, 사건 등이 포함된다
```
* Compound nouns are tagged with the largest span:
```
복합명사인 경우 가장 넓은 단위로 태깅해주세요 ex) [상하이] [디즈니랜드] -> [상하이 디즈니랜드]
```
* Final result is created by merging annotations from two separate annotators.

#### Phase II
* For each mention, a list of candidates from the knowledge base are shown. The annotator can select a candidate, not in candidate list, or not an entity.
* Each document was annotated by a single annotator.

#### Phase III
* For each mention, the annotator can select a preceding mention, no antecedent, or error. Noun phrases and pronouns are extracted using the parse information.
* "We scaled down the coreference resolution by limiting the scope of the target mentions to a named entity, pronoun, and definite noun phrase."
* Postfixes particles (조사) are not included in the antecedent:
```
[작업대상] 아래 항목에서 조사등을 제외(교정)해 주세요. 그녀는 -> 그녀
```

## Citation
```
@inproceedings{nam-etal-2020-effective,
    title = "Effective Crowdsourcing of Multiple Tasks for Comprehensive Knowledge Extraction",
    author = "Nam, Sangha  and
      Lee, Minho  and
      Kim, Donghwan  and
      Han, Kijong  and
      Kim, Kuntae  and
      Yoon, Sooji  and
      Kim, Eun-kyung  and
      Choi, Key-Sun",
    editor = "Calzolari, Nicoletta  and
      B{\'e}chet, Fr{\'e}d{\'e}ric  and
      Blache, Philippe  and
      Choukri, Khalid  and
      Cieri, Christopher  and
      Declerck, Thierry  and
      Goggi, Sara  and
      Isahara, Hitoshi  and
      Maegaard, Bente  and
      Mariani, Joseph  and
      Mazo, H{\'e}l{\`e}ne  and
      Moreno, Asuncion  and
      Odijk, Jan  and
      Piperidis, Stelios",
    booktitle = "Proceedings of the Twelfth Language Resources and Evaluation Conference",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://aclanthology.org/2020.lrec-1.27",
    pages = "212--219",
    abstract = "Information extraction from unstructured texts plays a vital role in the field of natural language processing. Although there has been extensive research into each information extraction task (i.e., entity linking, coreference resolution, and relation extraction), data are not available for a continuous and coherent evaluation of all information extraction tasks in a comprehensive framework. Given that each task is performed and evaluated with a different dataset, analyzing the effect of the previous task on the next task with a single dataset throughout the information extraction process is impossible. This paper aims to propose a Korean information extraction initiative point and promote research in this field by presenting crowdsourcing data collected for four information extraction tasks from the same corpus and the training and evaluation results for each task of a state-of-the-art model. These machine learning data for Korean information extraction are the first of their kind, and there are plans to continuously increase the data volume. The test results will serve as an initiative result for each Korean information extraction task and are expected to serve as a comparison target for various studies on Korean information extraction using the data collected in this study.",
    language = "English",
    ISBN = "979-10-95546-34-4",
}
```