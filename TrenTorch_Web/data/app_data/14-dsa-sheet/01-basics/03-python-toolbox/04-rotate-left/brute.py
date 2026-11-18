def rotate_left(nums, k):
    out = list(nums)
    if not out:
        return out
    for _ in range(k % len(out)):
        out.append(out.pop(0))
    return out
