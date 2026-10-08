def sync_steps(total, k):
    return [t for t in range(1, total + 1) if t % k == 0]
