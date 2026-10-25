def subsets_with_duplicates(nums):
    a = sorted(nums)
    out = []

    def go(start, current):
        out.append(list(current))
        for j in range(start, len(a)):
            if j > start and a[j] == a[j - 1]:
                continue
            current.append(a[j])
            go(j + 1, current)
            current.pop()

    go(0, [])
    return out
