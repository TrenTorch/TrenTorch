def block_table_lookup(block_table, token_idx, block_size):
    """
    block_table: physical block id for each logical block of the sequence
    token_idx: logical position of the token
    block_size: tokens per block

    Returns:
        (physical_block_id, offset_within_block) for the token.
    """
    # TODO: Map the token to its logical block, look up the physical block, and find the offset (see Theory).
    pass
