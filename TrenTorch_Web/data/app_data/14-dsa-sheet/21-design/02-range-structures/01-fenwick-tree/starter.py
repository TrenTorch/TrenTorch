def run_fenwick(nums: list[int], ops: list[str]) -> list[int]:
    """Run the updates and range sum queries."""
    # This is correct but too slow: every sum adds up the whole range again.
    values = list(nums)
    out = []
    for op in ops:
        parts = op.split()
        if parts[0] == "set":
            values[int(parts[1])] = int(parts[2])
        else:
            out.append(sum(values[int(parts[1]) : int(parts[2]) + 1]))
    return out
