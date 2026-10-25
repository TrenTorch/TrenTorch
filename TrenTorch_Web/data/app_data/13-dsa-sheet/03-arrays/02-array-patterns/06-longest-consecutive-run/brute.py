def longest_consecutive(nums):
    ordered = sorted(set(nums))
    best = run = 0
    for i, x in enumerate(ordered):
        run = run + 1 if i and ordered[i - 1] == x - 1 else 1
        best = max(best, run)
    return best
