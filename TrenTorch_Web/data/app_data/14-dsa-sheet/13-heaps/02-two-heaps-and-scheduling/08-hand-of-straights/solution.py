import heapq


def is_n_straight_hand(hand, group_size):
    if len(hand) % group_size:
        return False
    count = {}
    for x in hand:
        count[x] = count.get(x, 0) + 1
    heap = list(count)
    heapq.heapify(heap)
    while heap:
        start = heap[0]
        for x in range(start, start + group_size):
            if count.get(x, 0) == 0:
                return False
            count[x] -= 1
            if count[x] == 0:
                if x != heap[0]:
                    return False
                heapq.heappop(heap)
    return True
