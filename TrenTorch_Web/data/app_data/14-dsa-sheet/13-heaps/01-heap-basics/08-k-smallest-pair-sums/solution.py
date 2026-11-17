import heapq


def k_smallest_pair_sums(nums1, nums2, k):
    if not nums1 or not nums2 or k <= 0:
        return []
    heap = [(nums1[i] + nums2[0], i, 0) for i in range(min(len(nums1), k))]
    heapq.heapify(heap)
    out = []
    while heap and len(out) < k:
        total, i, j = heapq.heappop(heap)
        out.append(total)
        if j + 1 < len(nums2):
            heapq.heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))
    return out
