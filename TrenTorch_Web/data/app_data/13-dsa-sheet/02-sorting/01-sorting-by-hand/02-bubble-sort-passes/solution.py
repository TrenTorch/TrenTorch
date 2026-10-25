def bubble_sort_passes(nums):
    a = list(nums)
    passes = 0
    while True:
        passes += 1
        swapped = False
        for i in range(len(a) - 1):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                swapped = True
        if not swapped:
            return passes
