import heapq


def nth_ugly_number(n):
    heap = [1]
    seen = {1}
    x = 1
    for _ in range(n):
        x = heapq.heappop(heap)
        for p in (2, 3, 5):
            if x * p not in seen:
                seen.add(x * p)
                heapq.heappush(heap, x * p)
    return x
