def rearrange_by_sign(nums):
    pos = [x for x in nums if x >= 0]
    neg = [x for x in nums if x < 0]
    out = []
    for i in range(max(len(pos), len(neg))):
        if i < len(pos):
            out.append(pos[i])
        if i < len(neg):
            out.append(neg[i])
    return out
