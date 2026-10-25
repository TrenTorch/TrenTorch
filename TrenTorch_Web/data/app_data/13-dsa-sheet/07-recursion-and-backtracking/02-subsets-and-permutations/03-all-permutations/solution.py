def all_permutations(nums):
    a = sorted(nums)
    used = [False] * len(a)
    out = []
    current = []

    def go():
        if len(current) == len(a):
            out.append(list(current))
            return
        for j in range(len(a)):
            if used[j]:
                continue
            used[j] = True
            current.append(a[j])
            go()
            current.pop()
            used[j] = False

    go()
    return out
