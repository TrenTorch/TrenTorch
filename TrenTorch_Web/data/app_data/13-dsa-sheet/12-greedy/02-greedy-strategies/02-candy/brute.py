def candy(ratings):
    n = len(ratings)
    give = [1] * n
    changed = True
    while changed:
        changed = False
        for i in range(n):
            for j in (i - 1, i + 1):
                if 0 <= j < n and ratings[i] > ratings[j] and give[i] <= give[j]:
                    give[i] = give[j] + 1
                    changed = True
    return sum(give)
