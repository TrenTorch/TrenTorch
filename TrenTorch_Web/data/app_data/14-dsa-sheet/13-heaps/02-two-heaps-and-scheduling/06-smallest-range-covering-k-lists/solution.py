import heapq


def smallest_range(lists):
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists)]
    heapq.heapify(heap)
    current_max = max(lst[0] for lst in lists)
    best = [heap[0][0], current_max]
    while True:
        value, i, j = heapq.heappop(heap)
        if (current_max - value, value) < (best[1] - best[0], best[0]):
            best = [value, current_max]
        if j + 1 == len(lists[i]):
            return best
        nxt = lists[i][j + 1]
        current_max = max(current_max, nxt)
        heapq.heappush(heap, (nxt, i, j + 1))
