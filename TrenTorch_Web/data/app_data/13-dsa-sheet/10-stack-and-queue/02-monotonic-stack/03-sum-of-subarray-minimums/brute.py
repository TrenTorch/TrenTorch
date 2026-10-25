def sum_subarray_mins(arr):
    total = 0
    for i in range(len(arr)):
        lowest = arr[i]
        for j in range(i, len(arr)):
            lowest = min(lowest, arr[j])
            total += lowest
    return total % (10**9 + 7)
