def trainable_mask(names, n_frozen):
    mask = []
    for name in names:
        parts = name.split(".")
        if parts[0] == "embed":
            mask.append(n_frozen < 1)
        elif parts[0] == "layers" and len(parts) > 1 and parts[1].isdigit():
            mask.append(int(parts[1]) >= n_frozen)
        else:
            mask.append(True)
    return mask


def count_trainable(sizes, mask):
    return int(sum(s for s, m in zip(sizes, mask) if m))


def fraction_trainable(sizes, mask):
    return count_trainable(sizes, mask) / sum(sizes)
