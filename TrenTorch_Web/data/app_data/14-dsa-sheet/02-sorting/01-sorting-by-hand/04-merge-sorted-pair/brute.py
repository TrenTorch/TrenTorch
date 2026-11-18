def merge_sorted_pair(a, b):
    left, right = list(a), list(b)
    merged = []
    comparisons = 0
    while left and right:
        comparisons += 1
        if left[0] <= right[0]:
            merged.append(left.pop(0))
        else:
            merged.append(right.pop(0))
    return [merged + left + right, comparisons]
