def insertion_sort_shifts(nums):
    rank = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}
    size = len(rank)
    tree = [0] * (size + 1)
    shifts = 0
    for seen, x in enumerate(nums):
        i = rank[x]
        not_bigger = 0
        while i > 0:
            not_bigger += tree[i]
            i -= i & -i
        shifts += seen - not_bigger
        i = rank[x]
        while i <= size:
            tree[i] += 1
            i += i & -i
    return shifts
