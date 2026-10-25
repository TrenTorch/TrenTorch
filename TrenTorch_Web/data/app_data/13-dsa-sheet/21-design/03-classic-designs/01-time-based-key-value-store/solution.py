from bisect import bisect_right


def run_time_map(ops):
    times = {}
    values = {}
    out = []
    for op in ops:
        parts = op.split()
        if parts[0] == "set":
            times.setdefault(parts[1], []).append(int(parts[3]))
            values.setdefault(parts[1], []).append(parts[2])
        else:
            key = parts[1]
            i = bisect_right(times.get(key, []), int(parts[2]))
            out.append(values[key][i - 1] if i else "")
    return out
