def naive_attention_hbm_bytes(n, bytes_per=2):
    """
    n: sequence length
    bytes_per: bytes per score value (2 for fp16)

    Returns:
        The bytes of the n-by-n score matrix that naive attention writes to GPU high-bandwidth memory.
    """
    # TODO: Multiply the number of score entries by the bytes per entry (see Theory).
    pass
