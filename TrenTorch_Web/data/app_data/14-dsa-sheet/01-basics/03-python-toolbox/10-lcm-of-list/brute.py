def lcm_of_list(nums):
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    result = 1
    for x in nums:
        result = result * x // gcd(result, x)
    return result
