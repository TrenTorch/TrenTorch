def can_finish(num_courses, prerequisites):
    done = set()
    changed = True
    while changed:
        changed = False
        for c in range(num_courses):
            if c not in done and all(
                pre in done for course, pre in prerequisites if course == c
            ):
                done.add(c)
                changed = True
    return len(done) == num_courses
