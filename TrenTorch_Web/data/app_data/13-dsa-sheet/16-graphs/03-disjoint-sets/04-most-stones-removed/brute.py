def remove_stones(stones):
    n = len(stones)
    seen = [False] * n
    groups = 0
    for s in range(n):
        if seen[s]:
            continue
        groups += 1
        seen[s] = True
        stack = [s]
        while stack:
            i = stack.pop()
            for j in range(n):
                if not seen[j] and (
                    stones[j][0] == stones[i][0] or stones[j][1] == stones[i][1]
                ):
                    seen[j] = True
                    stack.append(j)
    return n - groups
