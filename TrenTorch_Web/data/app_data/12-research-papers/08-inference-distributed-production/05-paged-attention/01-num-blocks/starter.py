def vllm_num_blocks(seq_len, block_size):
    """
    seq_len: number of tokens in the sequence so far
    block_size: tokens per KV-cache block

    Returns:
        The number of physical blocks the sequence needs, rounding up for a partly filled block.
    """
    # TODO: Round seq_len / block_size up to a whole number of blocks (see Theory).
    pass
