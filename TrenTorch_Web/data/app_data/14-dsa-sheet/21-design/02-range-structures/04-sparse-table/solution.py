def range_minimums(nums, queries):
    n = len(nums)
    table = [list(nums)]
    k = 1
    while 2**k <= n:
        prev = table[-1]
        half = 2 ** (k - 1)
        table.append(list(map(min, prev, prev[half:])))
        k += 1
    out = []
    for left, right in queries:
        level = (right - left + 1).bit_length() - 1
        row = table[level]
        out.append(min(row[left], row[right - 2**level + 1]))
    return out
