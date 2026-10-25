def keep_at_most_twice(nums):
    a = list(nums)
    write = 0
    for read in range(len(a)):
        if write < 2 or a[read] != a[write - 2]:
            a[write] = a[read]
            write += 1
    return a[:write]
