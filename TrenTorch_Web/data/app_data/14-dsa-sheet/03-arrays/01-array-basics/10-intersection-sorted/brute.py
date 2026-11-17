def intersection_sorted(a, b):
    rest = list(b)
    out = []
    for x in a:
        if x in rest:
            rest.remove(x)
            out.append(x)
    return sorted(out)
