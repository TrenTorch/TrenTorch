def longest_ones_after_flip(n):
    best = 0
    for flip in [None, *range(32)]:
        value = n if flip is None else n | (1 << flip)
        run = longest = 0
        for i in range(32):
            if (value >> i) & 1:
                run += 1
                longest = max(longest, run)
            else:
                run = 0
        best = max(best, longest)
    return best
