def run_union_find(n: int, ops: list[str]) -> list[int]:
    """Run the union, connected and size operations and return the answers of connected and size."""
    # This is correct but too slow: it relabels a whole group on every union.
    label = list(range(n))
    out = []
    for op in ops:
        parts = op.split()
        if parts[0] == "union":
            a, b = label[int(parts[1])], label[int(parts[2])]
            if a != b:
                for i in range(n):
                    if label[i] == a:
                        label[i] = b
        elif parts[0] == "connected":
            out.append(1 if label[int(parts[1])] == label[int(parts[2])] else 0)
        else:
            out.append(label.count(label[int(parts[1])]))
    return out
