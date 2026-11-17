from collections import OrderedDict


def run_lfu(capacity, ops):
    value = {}
    count = {}
    groups = {}
    low = 0

    def touch(key):
        nonlocal low
        c = count[key]
        del groups[c][key]
        if not groups[c]:
            del groups[c]
            if low == c:
                low += 1
        count[key] = c + 1
        groups.setdefault(c + 1, OrderedDict())[key] = None

    out = []
    for op in ops:
        parts = op.split()
        key = int(parts[1])
        if parts[0] == "get":
            if key in value:
                touch(key)
                out.append(value[key])
            else:
                out.append(-1)
        elif capacity > 0:
            if key in value:
                value[key] = int(parts[2])
                touch(key)
            else:
                if len(value) == capacity:
                    oldest, _ = groups[low].popitem(last=False)
                    if not groups[low]:
                        del groups[low]
                    del value[oldest]
                    del count[oldest]
                value[key] = int(parts[2])
                count[key] = 1
                groups.setdefault(1, OrderedDict())[key] = None
                low = 1
    return out
