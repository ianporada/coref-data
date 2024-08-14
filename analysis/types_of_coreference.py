import collections
import copy
import os
import shutil

import conll_transform



TEXT_COL = 1
XPOS_COL = 4
HEAD_COL = 6
DEPREL_COL = 7



def generic(mention, sentences):
    sent_id, start, end = mention
    sentence = sentences[sent_id]
    lines = sentence[start:end+1]
    # a/an determiner
    for x in lines:
        if x[TEXT_COL] in ['a', 'an'] and x[DEPREL_COL] == 'det':
            return True
    # bare plural
    # xpos = NNS and no determinant
    determinant = any([x[DEPREL_COL] == 'det' for x in lines])
    if determinant:
        return False
    # is head NNS
    possible_heads = []
    for line in lines:
        head_id = int(line[HEAD_COL]) if line[HEAD_COL] not in ['-', '_', 'None'] else 0
        head_idx = head_id - 1
        if head_idx < start or head_idx > end:
            possible_heads += [line]
    head = possible_heads[-1] if possible_heads else lines[-1]
    if head[XPOS_COL] == 'NNS':
        return True
    return False


def compound_modifier(mention, sentences):
    sent_id, start, end = mention
    sentence = sentences[sent_id]
    lines = sentence[start:end+1]
    return all([x[DEPREL_COL] in ['nn', 'compound'] for x in lines])


def line_to_head_idx(line):
    head_id = int(line[HEAD_COL]) if line[HEAD_COL] not in ['-', '_', 'None'] else 0
    head_idx = head_id - 1
    return head_idx


def are_in_cop_rel(mention1, mention2, sentence):
    _, m1s, m1e = mention1
    _, m2s, m2e = mention2
    # one has a nsubj relation whose head is inside the other
    # a cop exists in the sentence whose head is inside the same one
    cops = [x for x in sentence if x[DEPREL_COL] == 'cop']
    if not cops:
        return False
    
    m1lines = sentence[m1s:m1e+1]
    m2lines = sentence[m2s:m2e+1]
    m1subjs = [x for x in m1lines if x[DEPREL_COL] == 'nsubj']
    m2subjs = [x for x in m2lines if x[DEPREL_COL] == 'nsubj']
    if not m1subjs and not m2subjs:
        return False
    
    cop_head_idxs = [line_to_head_idx(x) for x in cops]
    
    m1subj_heads_idxs = [line_to_head_idx(x) for x in m1subjs]
    if any([idx >= m2s and idx <= m2e for idx in m1subj_heads_idxs]) and any([idx >= m2s and idx <= m2e for idx in cop_head_idxs]):
        return True
    
    
    m2subj_heads_idxs = [line_to_head_idx(x) for x in m2subjs]
    if any([idx >= m1s and idx <= m1e for idx in m2subj_heads_idxs]) and any([idx >= m1s and idx <= m1e for idx in cop_head_idxs]):
        return True

    return False


def copula(chain, sentences):
    new_chain = []
    
    neighbors = [(ni, nm)
                    for ni, nm in enumerate(chain)]
    
    for curr_i, mention in enumerate(chain):
        sid, start, end = mention
        sentence = sentences[sid]
        for neighbor_i, neighbor_mention in neighbors:
            nsid, nstart, nend = neighbor_mention
            if (neighbor_i == curr_i) or nsid != sid:
                continue
            if are_in_cop_rel(mention, neighbor_mention, sentence):
                new_chain.append(mention)
                break
    
    return new_chain
