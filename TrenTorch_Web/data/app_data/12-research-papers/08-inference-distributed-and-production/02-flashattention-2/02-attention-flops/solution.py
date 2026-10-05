def attention_flops(n, d, causal=False):
    f = 4 * n * n * d
    return f // 2 if causal else f
