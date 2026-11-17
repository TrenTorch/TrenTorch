def merge_sorted_lists(lists):
    out = []
    for part in lists:
        out.extend(part)
    return sorted(out)
