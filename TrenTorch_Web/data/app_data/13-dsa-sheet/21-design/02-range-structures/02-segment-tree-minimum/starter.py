def run_segment_tree(nums: list[int], ops: list[str]) -> list[int]:
    """Run the updates and range minimum queries."""
    # This is correct but too slow: every query looks at the whole range again.
    values = list(nums)
    out = []
    for op in ops:
        parts = op.split()
        if parts[0] == "set":
            values[int(parts[1])] = int(parts[2])
        else:
            out.append(min(values[int(parts[1]) : int(parts[2]) + 1]))
    return out
