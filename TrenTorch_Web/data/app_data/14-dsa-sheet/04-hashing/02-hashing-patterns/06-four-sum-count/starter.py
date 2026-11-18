def four_sum_count(a, b, c, d):
    """Count the tuples (i, j, k, l) with a[i] + b[j] + c[k] + d[l] == 0."""
    # This is correct but far too slow: it tries every tuple.
    count = 0
    for x in a:
        for y in b:
            for z in c:
                for w in d:
                    if x + y + z + w == 0:
                        count += 1
    return count
