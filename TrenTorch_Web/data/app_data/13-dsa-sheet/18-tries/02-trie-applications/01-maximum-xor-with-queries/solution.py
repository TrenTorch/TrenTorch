def max_xor_queries(nums, queries):
    root = {}
    for n in nums:
        node = root
        for b in range(29, -1, -1):
            node = node.setdefault(n >> b & 1, {})
    out = []
    for x in queries:
        node = root
        best = 0
        for b in range(29, -1, -1):
            bit = x >> b & 1
            if 1 - bit in node:
                best |= 1 << b
                node = node[1 - bit]
            else:
                node = node[bit]
        out.append(best)
    return out
