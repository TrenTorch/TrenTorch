def union_sorted(a, b):
    out = []
    i = j = 0
    while i < len(a) or j < len(b):
        if j == len(b) or (i < len(a) and a[i] <= b[j]):
            x = a[i]
            i += 1
        else:
            x = b[j]
            j += 1
        if not out or out[-1] != x:
            out.append(x)
    return out
