def run_snapshot_array(length, ops):
    values = [0] * length
    snaps = []
    out = []
    for op in ops:
        parts = op.split()
        if parts[0] == "set":
            values[int(parts[1])] = int(parts[2])
        elif parts[0] == "snap":
            snaps.append(list(values))
            out.append(len(snaps) - 1)
        else:
            out.append(snaps[int(parts[2])][int(parts[1])])
    return out
