def frequency_extremes(nums):
    values = sorted(set(nums))
    table = [(nums.count(v), v) for v in values]
    most = max(table, key=lambda t: (t[0], -t[1]))[1]
    least = min(table)[1]
    return [most, least]
