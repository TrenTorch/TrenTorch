def make_connected(n, connections):
    if len(connections) < n - 1:
        return -1
    label = list(range(n))
    changed = True
    while changed:
        changed = False
        for a, b in connections:
            low = min(label[a], label[b])
            if label[a] != low or label[b] != low:
                label[a] = label[b] = low
                changed = True
    return len(set(label)) - 1
