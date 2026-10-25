def min_add_to_make_valid(s):
    open_count = need = 0
    for ch in s:
        if ch == "(":
            open_count += 1
        elif open_count:
            open_count -= 1
        else:
            need += 1
    return need + open_count
