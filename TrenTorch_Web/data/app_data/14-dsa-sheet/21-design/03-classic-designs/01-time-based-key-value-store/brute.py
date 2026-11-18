def run_time_map(ops):
    store = {}
    out = []
    for op in ops:
        parts = op.split()
        if parts[0] == "set":
            store.setdefault(parts[1], []).append((int(parts[3]), parts[2]))
        else:
            best = ""
            for time, value in store.get(parts[1], ()):
                if time <= int(parts[2]):
                    best = value
            out.append(best)
    return out
