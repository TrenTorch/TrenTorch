def run_range_add(n: int, ops: list[str]) -> list[int]:
    """Run the range additions and point queries on a list of zeros."""
    # This is correct but too slow: every addition touches each number of the range.
    values = [0] * n
    out = []
    for op in ops:
        parts = op.split()
        if parts[0] == "add":
            for i in range(int(parts[1]), int(parts[2]) + 1):
                values[i] += int(parts[3])
        else:
            out.append(values[int(parts[1])])
    return out
