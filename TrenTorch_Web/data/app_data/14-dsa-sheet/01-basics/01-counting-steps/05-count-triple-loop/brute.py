def count_triple_loop(n):
    count = 0
    for i in range(n):
        for j in range(i, n):
            for k in range(j, n):
                count += 1
    return count
