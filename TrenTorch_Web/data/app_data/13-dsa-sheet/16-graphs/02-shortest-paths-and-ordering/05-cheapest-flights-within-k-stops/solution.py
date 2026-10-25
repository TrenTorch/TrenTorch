def cheapest_price(n, flights, src, dst, k):
    inf = float("inf")
    best = [inf] * n
    best[src] = 0
    for _ in range(k + 1):
        nxt = best[:]
        for a, b, price in flights:
            if best[a] + price < nxt[b]:
                nxt[b] = best[a] + price
        best = nxt
    return best[dst] if best[dst] < inf else -1
