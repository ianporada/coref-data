"""Functions for detokenizing text"""

from nltk.tokenize.treebank import TreebankWordDetokenizer


detokenizer = TreebankWordDetokenizer()


def detokenize(tokens: dict) -> str:
    return detokenize_list([x["text"] for x in tokens])


def detokenize_list(tokens: list[str]) -> str:
    return detokenizer.detokenize(tokens)


def detokenize_sentences(sentences: dict) -> str:
    return detokenize_sentence_strings([x["text"] for x in sentences])


def detokenize_sentence_strings(sentences: list[str]) -> str:
    return " ".join(sentences)
