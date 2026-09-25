def is_subset(a, b):
    return a.issubset(b)


def argmax(values):
    best_index = 0
    best_value = values[0]
    for i, v in enumerate(values):
        if v > best_value:
            best_value = v
            best_index = i
    return best_index
