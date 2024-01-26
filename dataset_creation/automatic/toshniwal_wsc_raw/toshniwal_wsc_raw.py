# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors.
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
"""The Winograd Schema Challenge Dataset

Modified from:
https://github.com/shtoshni/fast-coref/blob/527e3a1c73719ae7443945f12237bcd97b84572f/src/data_processing/process_wsc.py
"""

import xml.etree.ElementTree as ET

import datasets

_DESCRIPTION = "WSC reformatted as coreference"
_DOWNLOAD_URL = "https://cs.nyu.edu/faculty/davise/papers/WinogradSchemas/WSCollection.xml"
_TOTAL_INSTANCES = 273

def search_span(word_list, token_list):
    for start_idx in range(0, len(word_list) - len(token_list) + 1):
        match = start_idx
        for token1, token2 in zip(
            word_list[start_idx : start_idx + len(token_list)], token_list
        ):
            if token1 != token2:
                match = -1
                break
        if match == -1:
            continue
        else:
            return match
    return -1


def tokenize(text):
    return text.split(" ")


def minimize_split(input_path):
    not_found_count = 0
    instances_processed = 0

    tree = ET.parse(input_path)
    root = tree.getroot()

    prefixes = []
    pronouns = []
    continuations = []

    answers = []
    correct_answers = []

    # write output
    num_tokens_list = []
    ment_len_list = []

    for elem in list(root)[:_TOTAL_INSTANCES]:
        for children in list(elem.iter("txt1")):
            prefix = children.text.strip().replace("\n", " ")
            prefixes.append(prefix)

        for children in list(elem.iter("pron")):
            pronouns.append(children.text.strip())

        for children in list(elem.iter("txt2")):
            continuations.append(children.text.strip())

        for children in list(elem.iter("answer")):
            answers.append(children.text.strip())

        for children in list(elem.iter("correctAnswer")):
            correct_answers.append(children.text.strip()[0])

    
    for idx, prefix in enumerate(prefixes):
        answer1 = answers[idx * 2]
        answer2 = answers[idx * 2 + 1]

        text = f"{prefix} {pronouns[idx * 2]} {continuations[idx]}"

        word_list = tokenize(prefix)
        prefix_idx = len(word_list)
        word_list += tokenize(pronouns[idx * 2])

        pronoun_boundary = [prefix_idx, len(word_list) - 1]
        word_list += tokenize(continuations[idx])

        answer_boundaries = []

        for answer in [answer1, answer2]:
            for span in [answer, answer.lower(), answer.capitalize()]:
                span_tokens = tokenize(span)
                found = search_span(word_list, span_tokens)
                if found != -1:
                    answer_boundaries.append([found, found + len(span_tokens) - 1])
                    break

            if found == -1:
                print(text, answer)
                not_found_count += 1

        if len(answer_boundaries) == 2:
            features = {}
            num_tokens_list.append(len(text.split()))

            ment_len_list.extend([1, len(answer1.split()), len(answer2.split())])

            correct_answer = correct_answers[idx]
            assert correct_answer in ["A", "B"]

            if correct_answer == "A":
                features["a_label"] = 1
            else:
                features["b_label"] = 1

            features["tokens"] = word_list

            features["pronoun_span"] = pronoun_boundary
            features["a_span"] = answer_boundaries[0]
            features["b_span"] = answer_boundaries[1]

            instances_processed += 1

            yield idx, features


class WinogradWSC(datasets.GeneratorBasedBuilder):
    """The Winograd Schema Challenge Dataset"""

    BUILDER_CONFIG_CLASS = datasets.BuilderConfig
    BUILDER_CONFIGS = [
        BUILDER_CONFIG_CLASS(),
    ]

    def _split_generators(self, dl_manager):
        path = dl_manager.download_and_extract(_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": path}),
        ]
    
    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
        )

    def _generate_examples(self, filepath):
        return minimize_split(filepath)
