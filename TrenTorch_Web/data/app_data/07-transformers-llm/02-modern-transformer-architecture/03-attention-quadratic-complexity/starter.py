def attention_compute_cost(seq_len: int, d_model: int) -> int:
    """
    Approximate multiply-add count for one self-attention layer's two
    big matrix multiplies (Q @ K^T, producing the (seq_len, seq_len)
    score matrix, and weights @ V, producing the output), for a SINGLE
    attention head's worth of `d_model` (summed across heads, the total
    is the same, since splitting `d_model` into heads doesn't change the
    total work, only how it's organized).
    """
    pass


def attention_memory_elements(seq_len: int, num_heads: int) -> int:
    """
    Number of scalar entries in the fully-materialized attention weight
    tensor, shape (num_heads, seq_len, seq_len).
    """
    pass


def ffn_compute_cost(seq_len: int, d_model: int, d_ff: int) -> int:
    """
    Approximate multiply-add count for the feed-forward sublayer's two
    linear layers (`[01-transformer-block/04-feedforward-sublayer]`),
    across all `seq_len` positions.
    """
    pass
