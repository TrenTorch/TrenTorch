import random


def k_smallest(nums, k):
    if k <= 0:
        return []
    if k >= len(nums):
        return sorted(nums)
    chosen = []
    pool = list(nums)
    need = k
    while need > 0:
        pivot = random.choice(pool)
        less = [x for x in pool if x < pivot]
        equal = [x for x in pool if x == pivot]
        if need <= len(less):
            pool = less
        elif need <= len(less) + len(equal):
            chosen += less
            chosen += equal[: need - len(less)]
            need = 0
        else:
            chosen += less
            chosen += equal
            need -= len(less) + len(equal)
            pool = [x for x in pool if x > pivot]
    return sorted(chosen)
