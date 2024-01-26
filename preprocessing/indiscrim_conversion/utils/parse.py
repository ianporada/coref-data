"""
Syntactic parsing.
"""

import stanza


nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma,depparse', logging_level="WARN")


def parse(text):
    return nlp(text).to_dict()
