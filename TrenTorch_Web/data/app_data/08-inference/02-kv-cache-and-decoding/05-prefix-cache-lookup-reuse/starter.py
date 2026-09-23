def prefix_cache_lookup(tokens: list, block_size: int, cache_store: list) -> dict:
    """
    tokens: list of token ids for the new request.
    cache_store: previously seen chained block hashes (from earlier requests).

    Returns a dict with keys "blocks_reused", "reused_tokens",
    "tokens_to_prefill", and "updated_cache_store".
    """
    # TODO: Split tokens into complete blocks of block_size, compute a
    # chained hash per block (each depends on the previous hash), walk
    # forward while each hash is already in cache_store, stop at the
    # first miss. See Theory for the chaining formula.
    pass
