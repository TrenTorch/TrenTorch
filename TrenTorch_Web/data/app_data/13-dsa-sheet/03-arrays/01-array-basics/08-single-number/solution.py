from functools import reduce
from operator import xor


def single_number(nums):
    return reduce(xor, nums)
