def all_subsets(nums):
    a = sorted(nums)
    out = []

    def go(start, current):
        out.append(list(current))
        for j in range(start, len(a)):
            current.append(a[j])
            go(j + 1, current)
            current.pop()

    go(0, [])
    return out
