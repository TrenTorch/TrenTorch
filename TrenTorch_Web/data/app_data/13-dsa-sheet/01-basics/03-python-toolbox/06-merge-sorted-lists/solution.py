import heapq


def merge_sorted_lists(lists):
    return list(heapq.merge(*lists))
