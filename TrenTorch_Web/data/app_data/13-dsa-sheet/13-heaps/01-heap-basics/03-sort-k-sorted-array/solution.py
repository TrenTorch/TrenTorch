import heapq


def sort_k_sorted(nums, k):
    heap = nums[: k + 1]
    heapq.heapify(heap)
    out = []
    for x in nums[k + 1 :]:
        out.append(heapq.heappushpop(heap, x))
    while heap:
        out.append(heapq.heappop(heap))
    return out
