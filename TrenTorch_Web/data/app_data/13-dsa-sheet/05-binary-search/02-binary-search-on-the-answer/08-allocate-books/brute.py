def allocate_books(pages, students):
    if students > len(pages):
        return -1
    for limit in range(max(pages), sum(pages) + 1):
        needed, load = 1, 0
        for p in pages:
            if load + p > limit:
                needed += 1
                load = 0
            load += p
        if needed <= students:
            return limit
