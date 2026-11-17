import math
from functools import reduce


def lcm_of_list(nums):
    return reduce(math.lcm, nums, 1)
