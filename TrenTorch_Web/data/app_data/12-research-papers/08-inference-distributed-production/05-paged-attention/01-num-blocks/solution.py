def vllm_num_blocks(seq_len, block_size):
    return -(-seq_len // block_size)
