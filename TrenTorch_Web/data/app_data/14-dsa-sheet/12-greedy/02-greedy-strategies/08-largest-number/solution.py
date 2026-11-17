from functools import cmp_to_key


def largest_number(nums):
    strings = [str(x) for x in nums]
    strings.sort(
        key=cmp_to_key(
            lambda a, b: -1 if a + b > b + a else (1 if a + b < b + a else 0)
        )
    )
    result = "".join(strings)
    return "0" if not result or result[0] == "0" else result
