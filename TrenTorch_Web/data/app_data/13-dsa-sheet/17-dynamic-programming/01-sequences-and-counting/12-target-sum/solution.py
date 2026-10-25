def find_target_sum_ways(nums, target):
    ways = {0: 1}
    for x in nums:
        nxt = {}
        for s, count in ways.items():
            nxt[s + x] = nxt.get(s + x, 0) + count
            nxt[s - x] = nxt.get(s - x, 0) + count
        ways = nxt
    return ways.get(target, 0)
