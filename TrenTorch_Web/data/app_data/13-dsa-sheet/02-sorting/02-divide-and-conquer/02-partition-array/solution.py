def partition_array(nums):
    a = list(nums)
    pivot = a[-1]
    i = -1
    for j in range(len(a) - 1):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[-1] = a[-1], a[i + 1]
    return [a, i + 1]
