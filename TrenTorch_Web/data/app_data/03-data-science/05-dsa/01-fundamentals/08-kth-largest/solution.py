import heapq


def solve(nums, k):
    """Return the k-th largest element of nums using a min-heap of size k."""
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]
