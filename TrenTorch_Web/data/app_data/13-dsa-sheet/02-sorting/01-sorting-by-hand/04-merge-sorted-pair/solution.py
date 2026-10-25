def merge_sorted_pair(a, b):
    merged = []
    i = j = comparisons = 0
    while i < len(a) and j < len(b):
        comparisons += 1
        if a[i] <= b[j]:
            merged.append(a[i])
            i += 1
        else:
            merged.append(b[j])
            j += 1
    merged.extend(a[i:])
    merged.extend(b[j:])
    return [merged, comparisons]
