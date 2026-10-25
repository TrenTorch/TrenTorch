import heapq


def kth_largest_stream(k, nums, adds):
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    out = []
    for x in adds:
        if len(heap) < k:
            heapq.heappush(heap, x)
        else:
            heapq.heappushpop(heap, x)
        out.append(heap[0])
    return out
