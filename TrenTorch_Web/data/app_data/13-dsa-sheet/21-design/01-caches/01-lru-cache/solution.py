from collections import OrderedDict


def run_lru(capacity, ops):
    cache = OrderedDict()
    out = []
    for op in ops:
        parts = op.split()
        if parts[0] == "get":
            key = int(parts[1])
            if key in cache:
                cache.move_to_end(key)
                out.append(cache[key])
            else:
                out.append(-1)
        elif capacity > 0:
            key, value = int(parts[1]), int(parts[2])
            if key in cache:
                cache.move_to_end(key)
            elif len(cache) == capacity:
                cache.popitem(last=False)
            cache[key] = value
    return out
