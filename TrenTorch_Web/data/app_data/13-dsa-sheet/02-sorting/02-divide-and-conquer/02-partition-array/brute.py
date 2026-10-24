def partition_array(nums):
    a = list(nums)
    last = len(a) - 1
    pivot = a[last]
    boundary = 0
    j = 0
    while j < last:
        if a[j] <= pivot:
            a[boundary], a[j] = a[j], a[boundary]
            boundary += 1
        j += 1
    a[boundary], a[last] = a[last], a[boundary]
    return [a, boundary]
