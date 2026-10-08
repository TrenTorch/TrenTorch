import numpy as np


def bert_input_embedding(token_ids, segment_ids, tok_table, seg_table, pos_table):
    """
    token_ids: token indices, shape (T,)
    segment_ids: segment index (0 or 1) per token, shape (T,)
    tok_table: token embedding table, shape (V, d)
    seg_table: segment embedding table, shape (2, d)
    pos_table: position embedding table, shape (max_len, d), with max_len >= T

    Returns:
        The input representation of shape (T, d): the sum of the three embeddings.
    """
    # TODO: Look up each embedding and sum them element-wise (see Theory).
    pass
