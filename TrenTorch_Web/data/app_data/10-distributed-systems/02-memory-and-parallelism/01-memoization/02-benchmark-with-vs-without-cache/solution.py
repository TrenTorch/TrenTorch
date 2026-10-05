def naive_kv_projection_work(prompt_len: int, num_new_tokens: int) -> int:
    total = 0
    for step in range(1, num_new_tokens + 1):
        current_len = prompt_len + step
        total += current_len
    return total


def cached_kv_projection_work(prompt_len: int, num_new_tokens: int) -> int:
    return prompt_len + num_new_tokens


def cache_work_reduction_factor(prompt_len: int, num_new_tokens: int) -> float:
    naive = naive_kv_projection_work(prompt_len, num_new_tokens)
    cached = cached_kv_projection_work(prompt_len, num_new_tokens)
    return naive / cached
