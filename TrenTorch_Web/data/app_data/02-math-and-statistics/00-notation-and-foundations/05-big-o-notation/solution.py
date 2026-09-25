def count_comparisons_linear_search(arr, target):
    comparisons = 0
    for value in arr:
        comparisons += 1
        if value == target:
            return True, comparisons
    return False, comparisons


def count_comparisons_binary_search(sorted_arr, target):
    lo, hi = 0, len(sorted_arr) - 1
    comparisons = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        comparisons += 1
        if sorted_arr[mid] == target:
            return True, comparisons
        elif sorted_arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False, comparisons
