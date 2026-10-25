def run_segment_tree(nums, ops):
    values = list(nums)
    out = []
    for op in ops:
        parts = op.split()
        if parts[0] == "set":
            values[int(parts[1])] = int(parts[2])
        else:
            out.append(min(values[int(parts[1]) : int(parts[2]) + 1]))
    return out
