import heapq


def k_smallest(nums, k):
    return heapq.nsmallest(k, nums)
