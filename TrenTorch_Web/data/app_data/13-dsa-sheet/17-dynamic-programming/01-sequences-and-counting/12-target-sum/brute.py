from itertools import product


def find_target_sum_ways(nums, target):
    return sum(
        1
        for signs in product((1, -1), repeat=len(nums))
        if sum(s * x for s, x in zip(signs, nums)) == target
    )
