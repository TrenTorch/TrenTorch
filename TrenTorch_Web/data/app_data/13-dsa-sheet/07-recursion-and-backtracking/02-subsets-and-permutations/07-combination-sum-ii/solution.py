def combination_sum_ii(candidates, target):
    a = sorted(candidates)
    out = []

    def go(start, remaining, current):
        if remaining == 0:
            out.append(list(current))
            return
        for j in range(start, len(a)):
            if j > start and a[j] == a[j - 1]:
                continue
            if a[j] > remaining:
                break
            current.append(a[j])
            go(j + 1, remaining - a[j], current)
            current.pop()

    go(0, target, [])
    return out
