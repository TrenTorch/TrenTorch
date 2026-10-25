def run_lru(capacity, ops):
    entries = []
    out = []
    for op in ops:
        parts = op.split()
        key = int(parts[1])
        index = next((i for i, (k, _) in enumerate(entries) if k == key), None)
        if parts[0] == "get":
            if index is None:
                out.append(-1)
            else:
                entry = entries.pop(index)
                entries.append(entry)
                out.append(entry[1])
        elif capacity > 0:
            if index is not None:
                entries.pop(index)
            elif len(entries) == capacity:
                entries.pop(0)
            entries.append((key, int(parts[2])))
    return out
