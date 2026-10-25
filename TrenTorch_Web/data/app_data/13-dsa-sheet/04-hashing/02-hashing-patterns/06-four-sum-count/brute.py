def four_sum_count(a, b, c, d):
    count = 0
    for x in a:
        for y in b:
            for z in c:
                for w in d:
                    if x + y + z + w == 0:
                        count += 1
    return count
