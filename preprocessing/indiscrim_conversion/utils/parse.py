"""
Syntactic parsing.
"""

import stanza


nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma,depparse', logging_level="WARN")

nlp_no_ssplit = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma,depparse', logging_level="WARN",
                      tokenize_no_ssplit=True)


def parse(text):
    return nlp(text).to_dict()


def parse_no_ssplit(text):
    """parse but don't split sentences"""
    return nlp_no_ssplit(text).to_dict()
