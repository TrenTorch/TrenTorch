def min_jumps(nums: list[int]) -> int:
    """Return the fewest jumps to reach the last index, or -1."""
    # This is correct but too slow: it fills in the best answer for every index from every earlier index.
    n = len(nums)
    if n <= 1:
        return 0
    INF = n + 1
    best = [INF] * n
    best[0] = 0
    for i in range(n):
        if best[i] == INF:
            continue
        for j in range(i + 1, min(n, i + nums[i] + 1)):
            if best[i] + 1 < best[j]:
                best[j] = best[i] + 1
    return best[n - 1] if best[n - 1] != INF else -1
