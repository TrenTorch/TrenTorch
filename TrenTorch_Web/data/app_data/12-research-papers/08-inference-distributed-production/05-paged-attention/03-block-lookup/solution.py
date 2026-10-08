def block_table_lookup(block_table, token_idx, block_size):
    return block_table[token_idx // block_size], token_idx % block_size
