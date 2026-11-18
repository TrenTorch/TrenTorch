def bubble_sort_passes(nums):
    a = list(nums)
    worst = 0
    for i in range(len(a)):
        worst = max(worst, sum(1 for x in a[:i] if x > a[i]))
    return worst + 1
