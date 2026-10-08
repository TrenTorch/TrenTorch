import numpy as np


def bert_input_embedding(token_ids, segment_ids, tok_table, seg_table, pos_table):
    T = len(token_ids)
    return tok_table[token_ids] + seg_table[segment_ids] + pos_table[:T]
