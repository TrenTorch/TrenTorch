def first_and_last(nums, target):
    found = [i for i, x in enumerate(nums) if x == target]
    return [found[0], found[-1]] if found else [-1, -1]
