import random


def kth_largest(nums, k):
    a = list(nums)
    target = len(a) - k
    while True:
        pivot = random.choice(a)
        less = [x for x in a if x < pivot]
        equal = a.count(pivot)
        if target < len(less):
            a = less
        elif target < len(less) + equal:
            return pivot
        else:
            target -= len(less) + equal
            a = [x for x in a if x > pivot]
