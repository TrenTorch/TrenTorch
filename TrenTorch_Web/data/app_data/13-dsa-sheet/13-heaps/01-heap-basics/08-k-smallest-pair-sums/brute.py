def k_smallest_pair_sums(nums1, nums2, k):
    return sorted(a + b for a in nums1 for b in nums2)[:k]
