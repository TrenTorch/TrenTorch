def run_lru(capacity: int, ops: list[str]) -> list[int]:
    """Run the cache operations and return the results of get."""
    # This is correct but too slow: it keeps the keys in a list and searches the list.
    order = []
    data = {}
    out = []
    for op in ops:
        parts = op.split()
        if parts[0] == "get":
            key = int(parts[1])
            if key in data:
                order.remove(key)
                order.append(key)
                out.append(data[key])
            else:
                out.append(-1)
        elif capacity > 0:
            key, value = int(parts[1]), int(parts[2])
            if key in data:
                order.remove(key)
            elif len(data) == capacity:
                del data[order.pop(0)]
            data[key] = value
            order.append(key)
    return out
