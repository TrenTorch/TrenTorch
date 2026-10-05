def attention_compute_cost(seq_len: int, d_model: int) -> int:
    return 2 * seq_len * seq_len * d_model


def attention_memory_elements(seq_len: int, num_heads: int) -> int:
    return num_heads * seq_len * seq_len


def ffn_compute_cost(seq_len: int, d_model: int, d_ff: int) -> int:
    return 2 * seq_len * d_model * d_ff
