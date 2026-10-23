from itertools import zip_longest


def rearrange_by_sign(nums):
    pos = [x for x in nums if x >= 0]
    neg = [x for x in nums if x < 0]
    return [x for pair in zip_longest(pos, neg) for x in pair if x is not None]
