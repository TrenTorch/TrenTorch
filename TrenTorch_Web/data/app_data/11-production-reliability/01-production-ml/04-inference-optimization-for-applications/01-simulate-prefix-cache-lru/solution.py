from collections import OrderedDict


def simulate_prefix_cache(capacity: int, requests: list[str]) -> list[bool]:
    cache: OrderedDict[str, None] = OrderedDict()
    hits = []
    for prefix in requests:
        if prefix in cache:
            hits.append(True)
            cache.move_to_end(prefix)
        else:
            hits.append(False)
            if len(cache) >= capacity:
                cache.popitem(last=False)
            cache[prefix] = None
    return hits
