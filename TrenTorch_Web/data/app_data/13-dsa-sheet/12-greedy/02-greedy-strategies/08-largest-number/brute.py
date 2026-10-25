from itertools import permutations


def largest_number(nums):
    if not nums:
        return "0"
    best = max("".join(map(str, p)) for p in permutations(nums))
    return "0" if best[0] == "0" else best
