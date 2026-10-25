def k_smallest_pair_sums(nums1: list[int], nums2: list[int], k: int) -> list[int]:
    """Return the k smallest sums a + b with a from nums1 and b from nums2."""
    # This is correct but too slow: it builds and sorts the sums of all pairs.
    return sorted(a + b for a in nums1 for b in nums2)[:k]
