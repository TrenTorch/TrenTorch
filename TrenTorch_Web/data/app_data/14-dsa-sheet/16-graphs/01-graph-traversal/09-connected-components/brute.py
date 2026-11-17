def count_components(n, edges):
    label = list(range(n))
    changed = True
    while changed:
        changed = False
        for a, b in edges:
            low = min(label[a], label[b])
            if label[a] != low or label[b] != low:
                label[a] = label[b] = low
                changed = True
    return len(set(label))
