def run_lfu(capacity, ops):
    data = {}
    clock = 0
    out = []
    for op in ops:
        parts = op.split()
        key = int(parts[1])
        clock += 1
        if parts[0] == "get":
            if key in data:
                value, count, _ = data[key]
                data[key] = (value, count + 1, clock)
                out.append(value)
            else:
                out.append(-1)
        elif capacity > 0:
            if key in data:
                _, count, _ = data[key]
                data[key] = (int(parts[2]), count + 1, clock)
            else:
                if len(data) == capacity:
                    victim = min(data, key=lambda k: (data[k][1], data[k][2]))
                    del data[victim]
                data[key] = (int(parts[2]), 1, clock)
    return out
