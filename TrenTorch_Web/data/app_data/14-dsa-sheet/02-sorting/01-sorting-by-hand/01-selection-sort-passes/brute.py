def selection_sort_passes(nums):
    a = list(nums)
    passes = []
    for i in range(max(len(a) - 1, 0)):
        index = a.index(min(a[i:]), i)
        a[i], a[index] = a[index], a[i]
        passes.append(a[:])
    return passes
