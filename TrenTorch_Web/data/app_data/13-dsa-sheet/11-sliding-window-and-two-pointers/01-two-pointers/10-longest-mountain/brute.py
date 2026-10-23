def longest_mountain(arr):
    n = len(arr)
    best = 0
    for i in range(n):
        for j in range(i + 2, n):
            part = arr[i : j + 1]
            peak = part.index(max(part))
            if (
                0 < peak < len(part) - 1
                and all(part[k] < part[k + 1] for k in range(peak))
                and all(part[k] > part[k + 1] for k in range(peak, len(part) - 1))
            ):
                best = max(best, len(part))
    return best
