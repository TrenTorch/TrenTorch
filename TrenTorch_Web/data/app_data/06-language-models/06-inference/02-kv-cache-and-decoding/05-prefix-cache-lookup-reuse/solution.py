def _chained_hashes(tokens, block_size):
    hashes = []
    prev = "SEED"
    for start in range(0, len(tokens) - len(tokens) % block_size, block_size):
        block = tuple(tokens[start : start + block_size])
        prev = hash((prev, block))
        hashes.append(prev)
    return hashes


def prefix_cache_lookup(tokens: list, block_size: int, cache_store: list) -> dict:
    cache_store = set(cache_store)
    hashes = _chained_hashes(tokens, block_size)

    blocks_reused = 0
    for h in hashes:
        if h in cache_store:
            blocks_reused += 1
        else:
            break

    reused_tokens = blocks_reused * block_size
    tokens_to_prefill = tokens[reused_tokens:]

    updated_store = cache_store | set(hashes)

    return {
        "blocks_reused": blocks_reused,
        "reused_tokens": reused_tokens,
        "tokens_to_prefill": tokens_to_prefill,
        "updated_cache_store": sorted(str(h) for h in updated_store),
    }
