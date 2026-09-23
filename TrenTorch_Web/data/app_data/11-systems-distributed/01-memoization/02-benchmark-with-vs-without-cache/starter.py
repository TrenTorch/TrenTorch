def naive_kv_projection_work(prompt_len: int, num_new_tokens: int) -> int:
    """
    01-kv-cache-autoregressive-generation's generate_without_cache
    reprojects K and V for the ENTIRE sequence-so-far, at every single
    generation step. Counting "one token projected through W_K (and
    W_V, counted together as one unit of work)" as one unit of work,
    this counts the TOTAL such units across all num_new_tokens steps.

    At step i (1-indexed), the current sequence length is
    prompt_len + i, and ALL of those tokens get reprojected.
    """
    # TODO: sum (prompt_len + step) for step in 1..num_new_tokens.
    pass


def cached_kv_projection_work(prompt_len: int, num_new_tokens: int) -> int:
    """
    With a cache, the prompt's K/V are projected exactly once (prefill,
    prompt_len units of work), and each new token contributes exactly
    one more unit of work for its own K/V -- previously-cached tokens
    are never reprojected.
    """
    # TODO: prompt_len + num_new_tokens.
    pass


def cache_work_reduction_factor(prompt_len: int, num_new_tokens: int) -> float:
    """
    Returns naive_kv_projection_work / cached_kv_projection_work -- how
    many times more K/V-projection work the naive, cache-free approach
    performs for the same generation task.
    """
    # TODO: call both functions above and divide.
    pass
