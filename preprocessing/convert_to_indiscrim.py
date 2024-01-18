"""
Convert raw datasets into the "indiscrim" (indiscriminate) coreference format

{
  "id": str, # example id
  "text": str, # untokenized example text
  "sentences": [
    {
      "id": int, # sentence index
      "text": str, # untokenized sentence text
      "speaker": None, # speaker
      "tokens": [
        {
          # keys are conllu columns: id, text, lemma, upos, xpos, feats, head, deprel, deps, misc
        },
        ...
      ]
    },
    ...
  ],
  "coref_chains": List[List[List[int]]], # list of clusters, each cluster is a list of mentions, each mention is a span represented as [sent, start, end] inclusive
  "genre": str,
  "meta_data": {
      "comment": str,
  },
}
"""

from .indiscrim_conversion.conll2012 import convert_conll2012




def main():
    convert_conll2012()


if __name__ == "__main__":
    main()