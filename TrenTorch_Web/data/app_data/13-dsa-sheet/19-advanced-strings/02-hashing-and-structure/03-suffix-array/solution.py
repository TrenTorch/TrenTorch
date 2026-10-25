def suffix_array(s):
    n = len(s)
    if n == 0:
        return []
    rank = [ord(c) for c in s]
    order = list(range(n))
    k = 1
    while True:

        def key(i):
            return (rank[i], rank[i + k] if i + k < n else -1)

        order.sort(key=key)
        new_rank = [0] * n
        for idx in range(1, n):
            new_rank[order[idx]] = new_rank[order[idx - 1]] + (
                key(order[idx]) != key(order[idx - 1])
            )
        rank = new_rank
        if rank[order[-1]] == n - 1:
            break
        k *= 2
    return order
