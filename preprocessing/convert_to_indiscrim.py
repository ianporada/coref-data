def span_to_ids(span):
  """Split span string into start and end ids"""
  if ".." in span:
    return span.split("..")
  return [span, span] # same start and end

def xml_sentence_spans(data_dir, document_name):
    """Parse sentence spans from xml file: [(word_start, word_end), ...]"""
    fname = os.path.join(data_dir, "markables", document_name + "_sentence_level.xml")

    sentence_spans = []
    for markable in ET.parse(fname).getroot().iter():
        if "id" not in markable.attrib:
            continue
        assert int(markable.attrib["orderid"]) == len(sentence_spans), "Sentence ids should be continuous"
        span = markable.attrib["span"]
        start, end = map(word_id_to_index, span_to_ids(span))
        sentence_spans.append((start, end))
    return sentence_spans


def xml_lemmas(data_dir, document_name):
    """Parse a list of lemmas from xml file"""
    fname = os.path.join(data_dir, "markables", document_name + "_morph_level.xml")

    lemmas = []
    for markable in ET.parse(fname).getroot().iter():
        if "id" not in markable.attrib:
            continue
        assert word_id_to_index(markable.attrib["span"]) == len(lemmas), "Words ids should be continuous"
        lemmas.append(markable.attrib["lemma"])
    return lemmas


def xml_pos_tags(data_dir, document_name):
    """Parse a list of pos tags from xml file"""
    fname = os.path.join(data_dir, "markables", document_name + "_pos_level.xml")

    pos_tags = []
    for markable in ET.parse(fname).getroot().iter():
        if "id" not in markable.attrib:
            continue
        assert word_id_to_index(markable.attrib["span"]) == len(pos_tags), "Words ids should be continuous"
        pos_tags.append(markable.attrib["tag"])
    return pos_tags

def xml_coref(data_dir, document_name):
    """Parse coref data from an xml file"""
    fname = os.path.join(data_dir, "markables", document_name + "_coref_level.xml")

    features = {}
    for markable in ET.parse(fname).getroot().iter():
        if "id" not in markable.attrib:
            continue

        if "coref_set" not in markable.attrib:
            continue # does not refer to a cluster

        # raw_span = markable.attrib["span"]
        # span = map(word_id_to_index, span_to_ids())
        # min_span = None
        # if "min_ids" in span.attrib:
        #     min_span = map(word_id_to_index, span_to_ids(markable.attrib["min_ids"]))
        # non_ref_type="coordination"

        markable_features = {
            "span": markable.attrib["span"],
            "min_span": markable.attrib["min_span"],
            "coref_set": markable.attrib["coref_set"], # set_{} which is the cluster id
            "generic": markable.attrib["generic"], # generic_no or something else
            "generic": markable.attrib["generic"], # generic_no or something else
            "person": markable.attrib["person"], # per1, per2, or per3 
            "related_object": markable.attrib["related_object"], # yes or no
            "grammatical_function": markable.attrib["gram_fnc"], # no-gf or function
            "number": markable.attrib["number"], # sing, plur, or mass
            "reference": markable.attrib["reference"], # old or new
            "gender": markable.attrib["gender"], # neut, fem, or masc
            "raw_features": markable.attrib,
        }
        features[markable.attrib["id"]] = markable_features
    return features