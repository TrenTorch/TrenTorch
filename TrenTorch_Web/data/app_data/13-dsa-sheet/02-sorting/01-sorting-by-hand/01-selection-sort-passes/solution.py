def selection_sort_passes(nums):
    a = list(nums)
    passes = []
    for i in range(len(a) - 1):
        smallest = i
        for j in range(i + 1, len(a)):
            if a[j] < a[smallest]:
                smallest = j
        a[i], a[smallest] = a[smallest], a[i]
        passes.append(list(a))
    return passes
