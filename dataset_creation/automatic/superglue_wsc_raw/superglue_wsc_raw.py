# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""The WSC from the SuperGLUE benchmark."""


import json
import os

import datasets


_SUPER_GLUE_CITATION = """\
@article{wang2019superglue,
  title={SuperGLUE: A Stickier Benchmark for General-Purpose Language Understanding Systems},
  author={Wang, Alex and Pruksachatkun, Yada and Nangia, Nikita and Singh, Amanpreet and Michael, Julian and Hill, Felix and Levy, Omer and Bowman, Samuel R},
  journal={arXiv preprint arXiv:1905.00537},
  year={2019}
}

Note that each SuperGLUE dataset has its own citation. Please see the source to
get the correct citation for each contained dataset.
"""

_GLUE_DESCRIPTION = """\
SuperGLUE (https://super.gluebenchmark.com/) is a new benchmark styled after
GLUE with a new set of more difficult language understanding tasks, improved
resources, and a new public leaderboard.

"""

_WSC_DESCRIPTION = """\
The Winograd Schema Challenge (WSC, Levesque et al., 2012) is a reading comprehension
task in which a system must read a sentence with a pronoun and select the referent of that pronoun
from a list of choices. Given the difficulty of this task and the headroom still left, we have included
WSC in SuperGLUE and recast the dataset into its coreference form. The task is cast as a binary
classification problem, as opposed to N-multiple choice, in order to isolate the model's ability to
understand the coreference links within a sentence as opposed to various other strategies that may
come into play in multiple choice conditions. With that in mind, we create a split with 65% negative
majority class in the validation set, reflecting the distribution of the hidden test set, and 52% negative
class in the training set. The training and validation examples are drawn from the original Winograd
Schema dataset (Levesque et al., 2012), as well as those distributed by the affiliated organization
Commonsense Reasoning. The test examples are derived from fiction books and have been shared
with us by the authors of the original dataset. Previously, a version of WSC recast as NLI as included
in GLUE, known as WNLI. No substantial progress was made on WNLI, with many submissions
opting to submit only majority class predictions. WNLI was made especially difficult due to an
adversarial train/dev split: Premise sentences that appeared in the training set sometimes appeared
in the development set with a different hypothesis and a flipped label. If a system memorized the
training set without meaningfully generalizing, which was easy due to the small size of the training
set, it could perform far below chance on the development set. We remove this adversarial design
in the SuperGLUE version of WSC by ensuring that no sentences are shared between the training,
validation, and test sets.

However, the validation and test sets come from different domains, with the validation set consisting
of ambiguous examples such that changing one non-noun phrase word will change the coreference
dependencies in the sentence. The test set consists only of more straightforward examples, with a
high number of noun phrases (and thus more choices for the model), but low to no ambiguity."""


_WSC_CITATION = """\
@inproceedings{levesque2012winograd,
  title={The winograd schema challenge},
  author={Levesque, Hector and Davis, Ernest and Morgenstern, Leora},
  booktitle={Thirteenth International Conference on the Principles of Knowledge Representation and Reasoning},
  year={2012}
}"""


class SuperGlueConfig(datasets.BuilderConfig):
    """BuilderConfig for SuperGLUE."""

    def __init__(self, features, data_url, citation, url, label_classes=("False", "True"), **kwargs):
        """BuilderConfig for SuperGLUE.

        Args:
          features: `list[string]`, list of the features that will appear in the
            feature dict. Should not include "label".
          data_url: `string`, url to download the zip file from.
          citation: `string`, citation for the data set.
          url: `string`, url for information about the data set.
          label_classes: `list[string]`, the list of classes for the label if the
            label is present as a string. Non-string labels will be cast to either
            'False' or 'True'.
          **kwargs: keyword arguments forwarded to super.
        """
        # Version history:
        # 1.0.3: Fix not including entity position in ReCoRD.
        # 1.0.2: Fixed non-nondeterminism in ReCoRD.
        # 1.0.1: Change from the pre-release trial version of SuperGLUE (v1.9) to
        #        the full release (v2.0).
        # 1.0.0: S3 (new shuffling, sharding and slicing mechanism).
        # 0.0.2: Initial version.
        super(SuperGlueConfig, self).__init__(version=datasets.Version("1.0.3"), **kwargs)
        self.features = features
        self.label_classes = label_classes
        self.data_url = data_url
        self.citation = citation
        self.url = url


class SuperGlue(datasets.GeneratorBasedBuilder):
    """The SuperGLUE benchmark."""

    BUILDER_CONFIGS = [
        SuperGlueConfig(
            name="wsc",
            description=_WSC_DESCRIPTION,
            # Note that span1_index and span2_index will be integers stored as
            # datasets.Value('int32').
            features=["text", "span1_index", "span2_index", "span1_text", "span2_text"],
            data_url="https://dl.fbaipublicfiles.com/glue/superglue/data/v2/WSC.zip",
            citation=_WSC_CITATION,
            url="https://cs.nyu.edu/faculty/davise/papers/WinogradSchemas/WS.html",
        ),
        SuperGlueConfig(
            name="wsc.fixed",
            description=(
                _WSC_DESCRIPTION + "\n\nThis version fixes issues where the spans are not actually "
                "substrings of the text."
            ),
            # Note that span1_index and span2_index will be integers stored as
            # datasets.Value('int32').
            features=["text", "span1_index", "span2_index", "span1_text", "span2_text"],
            data_url="https://dl.fbaipublicfiles.com/glue/superglue/data/v2/WSC.zip",
            citation=_WSC_CITATION,
            url="https://cs.nyu.edu/faculty/davise/papers/WinogradSchemas/WS.html",
        ),
    ]

    def _info(self):
        features = {feature: datasets.Value("string") for feature in self.config.features}
        if self.config.name.startswith("wsc"):
            features["span1_index"] = datasets.Value("int32")
            features["span2_index"] = datasets.Value("int32")
        if self.config.name == "wic":
            features["start1"] = datasets.Value("int32")
            features["start2"] = datasets.Value("int32")
            features["end1"] = datasets.Value("int32")
            features["end2"] = datasets.Value("int32")
        if self.config.name == "multirc":
            features["idx"] = dict(
                {
                    "paragraph": datasets.Value("int32"),
                    "question": datasets.Value("int32"),
                    "answer": datasets.Value("int32"),
                }
            )
        elif self.config.name == "record":
            features["idx"] = dict(
                {
                    "passage": datasets.Value("int32"),
                    "query": datasets.Value("int32"),
                }
            )
        else:
            features["idx"] = datasets.Value("int32")

        if self.config.name == "record":
            # Entities are the set of possible choices for the placeholder.
            features["entities"] = datasets.features.Sequence(datasets.Value("string"))
            # The start and end indices of paragraph text for each entity.
            features["entity_spans"] = datasets.features.Sequence(
                {
                    "text": datasets.Value("string"),
                    "start": datasets.Value("int32"),
                    "end": datasets.Value("int32"),
                }
            )
            # Answers are the subset of entities that are correct.
            features["answers"] = datasets.features.Sequence(datasets.Value("string"))
        else:
            features["label"] = datasets.features.ClassLabel(names=self.config.label_classes)

        return datasets.DatasetInfo(
            description=_GLUE_DESCRIPTION + self.config.description,
            features=datasets.Features(features),
            homepage=self.config.url,
            citation=self.config.citation + "\n" + _SUPER_GLUE_CITATION,
        )

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(self.config.data_url) or ""
        task_name = _get_task_name_from_data_url(self.config.data_url)
        dl_dir = os.path.join(dl_dir, task_name)
        if self.config.name in ["axb", "axg"]:
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "data_file": os.path.join(dl_dir, f"{task_name}.jsonl"),
                        "split": datasets.Split.TEST,
                    },
                ),
            ]
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "data_file": os.path.join(dl_dir, "train.jsonl"),
                    "split": datasets.Split.TRAIN,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "data_file": os.path.join(dl_dir, "val.jsonl"),
                    "split": datasets.Split.VALIDATION,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "data_file": os.path.join(dl_dir, "test.jsonl"),
                    "split": datasets.Split.TEST,
                },
            ),
        ]

    def _generate_examples(self, data_file, split):
        with open(data_file, encoding="utf-8") as f:
            for line in f:
                row = json.loads(line)

                if self.config.name == "multirc":
                    paragraph = row["passage"]
                    for question in paragraph["questions"]:
                        for answer in question["answers"]:
                            label = answer.get("label")
                            key = "%s_%s_%s" % (row["idx"], question["idx"], answer["idx"])
                            yield key, {
                                "paragraph": paragraph["text"],
                                "question": question["question"],
                                "answer": answer["text"],
                                "label": -1 if label is None else _cast_label(bool(label)),
                                "idx": {"paragraph": row["idx"], "question": question["idx"], "answer": answer["idx"]},
                            }
                elif self.config.name == "record":
                    passage = row["passage"]
                    entity_texts, entity_spans = _get_record_entities(passage)
                    for qa in row["qas"]:
                        yield qa["idx"], {
                            "passage": passage["text"],
                            "query": qa["query"],
                            "entities": entity_texts,
                            "entity_spans": entity_spans,
                            "answers": _get_record_answers(qa),
                            "idx": {"passage": row["idx"], "query": qa["idx"]},
                        }
                else:
                    if self.config.name.startswith("wsc"):
                        row.update(row["target"])
                    example = {feature: row[feature] for feature in self.config.features}
                    if self.config.name == "wsc.fixed":
                        example = _fix_wst(example)
                    example["idx"] = row["idx"]

                    if "label" in row:
                        if self.config.name == "copa":
                            example["label"] = "choice2" if row["label"] else "choice1"
                        else:
                            example["label"] = _cast_label(row["label"])
                    else:
                        assert split == datasets.Split.TEST, row
                        example["label"] = -1
                    yield example["idx"], example


def _fix_wst(ex):
    """Fixes most cases where spans are not actually substrings of text."""

    def _fix_span_text(k):
        """Fixes a single span."""
        text = ex[k + "_text"]
        index = ex[k + "_index"]

        if text in ex["text"]:
            return

        if text in ("Kamenev and Zinoviev", "Kamenev, Zinoviev, and Stalin"):
            # There is no way to correct these examples since the subjects have
            # intervening text.
            return

        if "theyscold" in text:
            ex["text"].replace("theyscold", "they scold")
            ex["span2_index"] = 10
        # Make sure case of the first words match.
        first_word = ex["text"].split()[index]
        if first_word[0].islower():
            text = text[0].lower() + text[1:]
        else:
            text = text[0].upper() + text[1:]
        # Remove punctuation in span.
        text = text.rstrip(".")
        # Replace incorrect whitespace character in span.
        text = text.replace("\n", " ")
        ex[k + "_text"] = text
        assert ex[k + "_text"] in ex["text"], ex

    _fix_span_text("span1")
    _fix_span_text("span2")
    return ex


def _cast_label(label):
    """Converts the label into the appropriate string version."""
    if isinstance(label, str):
        return label
    elif isinstance(label, bool):
        return "True" if label else "False"
    elif isinstance(label, int):
        assert label in (0, 1)
        return str(label)
    else:
        raise ValueError("Invalid label format.")


def _get_record_entities(passage):
    """Returns the unique set of entities."""
    text = passage["text"]
    entity_spans = list()
    for entity in passage["entities"]:
        entity_text = text[entity["start"] : entity["end"] + 1]
        entity_spans.append({"text": entity_text, "start": entity["start"], "end": entity["end"] + 1})
    entity_spans = sorted(entity_spans, key=lambda e: e["start"])  # sort by start index
    entity_texts = set(e["text"] for e in entity_spans)  # for backward compatability
    return entity_texts, entity_spans


def _get_record_answers(qa):
    """Returns the unique set of answers."""
    if "answers" not in qa:
        return []
    answers = set()
    for answer in qa["answers"]:
        answers.add(answer["text"])
    return sorted(answers)


def _get_task_name_from_data_url(data_url):
    return data_url.split("/")[-1].split(".")[0]