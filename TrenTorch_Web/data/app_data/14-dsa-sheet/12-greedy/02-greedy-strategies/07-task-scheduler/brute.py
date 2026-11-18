from collections import Counter


def least_interval(tasks, n):
    counts = Counter(tasks)
    next_free = {c: 0 for c in counts}
    remaining = len(tasks)
    time = 0
    while remaining:
        available = [c for c in counts if counts[c] > 0 and next_free[c] <= time]
        if available:
            c = max(available, key=lambda x: (counts[x], x))
            counts[c] -= 1
            next_free[c] = time + n + 1
            remaining -= 1
        time += 1
    return time
