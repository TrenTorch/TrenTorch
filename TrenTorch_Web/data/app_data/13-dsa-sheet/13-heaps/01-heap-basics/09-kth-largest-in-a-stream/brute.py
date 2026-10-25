def kth_largest_stream(k, nums, adds):
    values = list(nums)
    out = []
    for x in adds:
        values.append(x)
        out.append(sorted(values, reverse=True)[k - 1])
    return out
