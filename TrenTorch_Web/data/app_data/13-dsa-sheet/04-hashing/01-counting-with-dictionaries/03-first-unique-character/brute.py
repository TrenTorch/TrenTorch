def first_unique_character(s):
    for i, ch in enumerate(s):
        if s.count(ch) == 1:
            return i
    return -1
