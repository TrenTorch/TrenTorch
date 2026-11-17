def combination_sum(candidates, target):
    a = sorted(candidates)
    out = []

    def go(start, remaining, current):
        if remaining == 0:
            out.append(list(current))
            return
        for j in range(start, len(a)):
            if a[j] > remaining:
                break
            current.append(a[j])
            go(j, remaining - a[j], current)
            current.pop()

    go(0, target, [])
    return out
