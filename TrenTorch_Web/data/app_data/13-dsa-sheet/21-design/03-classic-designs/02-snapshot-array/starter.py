def run_snapshot_array(length: int, ops: list[str]) -> list[int]:
    """Run the operations and return the results of snap and get."""
    # This is correct but too slow: every get reads all the changes made so far.
    changes = []
    snaps = 0
    out = []
    for op in ops:
        parts = op.split()
        if parts[0] == "set":
            changes.append((snaps, int(parts[1]), int(parts[2])))
        elif parts[0] == "snap":
            out.append(snaps)
            snaps += 1
        else:
            value = 0
            for snap_id, i, v in changes:
                if i == int(parts[1]) and snap_id <= int(parts[2]):
                    value = v
            out.append(value)
    return out
