from bisect import bisect_right


def run_snapshot_array(length, ops):
    ids = {}
    vals = {}
    snap_id = 0
    out = []
    for op in ops:
        parts = op.split()
        if parts[0] == "set":
            i, v = int(parts[1]), int(parts[2])
            if i in ids and ids[i][-1] == snap_id:
                vals[i][-1] = v
            else:
                ids.setdefault(i, []).append(snap_id)
                vals.setdefault(i, []).append(v)
        elif parts[0] == "snap":
            out.append(snap_id)
            snap_id += 1
        else:
            i, want = int(parts[1]), int(parts[2])
            k = bisect_right(ids.get(i, []), want) - 1
            out.append(vals[i][k] if k >= 0 else 0)
    return out
