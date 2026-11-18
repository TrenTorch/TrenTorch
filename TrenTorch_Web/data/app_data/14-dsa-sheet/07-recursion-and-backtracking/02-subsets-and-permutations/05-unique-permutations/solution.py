def unique_permutations(nums):
    a = sorted(nums)
    used = [False] * len(a)
    out = []
    current = []

    def go():
        if len(current) == len(a):
            out.append(list(current))
            return
        for j in range(len(a)):
            if used[j] or (j > 0 and a[j] == a[j - 1] and not used[j - 1]):
                continue
            used[j] = True
            current.append(a[j])
            go()
            current.pop()
            used[j] = False

    go()
    return out
