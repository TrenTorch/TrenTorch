def simulate_prefix_cache(capacity: int, requests: list[str]) -> list[bool]:
    """Simulate an LRU-evicted prefix cache of the given `capacity` (number
    of distinct prefixes it can hold). Process `requests` (each one a
    prefix string) in order. For each one, return True if it was already in
    the cache (a hit) or False if it wasn't (a miss). A hit refreshes that
    prefix as most-recently-used. A miss inserts it as most-recently-used,
    evicting the least-recently-used entry first if the cache is full.
    """
    # TODO: implement
    pass
