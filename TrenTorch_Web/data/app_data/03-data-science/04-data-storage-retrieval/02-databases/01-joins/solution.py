def nested_loop_join(left: list, right: list, key: str) -> list:
    result = []
    for left_row in left:
        for right_row in right:
            if left_row[key] == right_row[key]:
                result.append({**left_row, **right_row})
    return result


def hash_join(left: list, right: list, key: str) -> list:
    index = {}
    for right_row in right:
        index.setdefault(right_row[key], []).append(right_row)
    result = []
    for left_row in left:
        for right_row in index.get(left_row[key], []):
            result.append({**left_row, **right_row})
    return result


def sort_merge_join(left: list, right: list, key: str) -> list:
    left_sorted = sorted(left, key=lambda row: row[key])
    right_sorted = sorted(right, key=lambda row: row[key])
    result = []
    i = j = 0
    while i < len(left_sorted) and j < len(right_sorted):
        left_key, right_key = left_sorted[i][key], right_sorted[j][key]
        if left_key < right_key:
            i += 1
        elif left_key > right_key:
            j += 1
        else:
            i_end = i
            while i_end < len(left_sorted) and left_sorted[i_end][key] == left_key:
                i_end += 1
            j_end = j
            while j_end < len(right_sorted) and right_sorted[j_end][key] == right_key:
                j_end += 1
            for left_row in left_sorted[i:i_end]:
                for right_row in right_sorted[j:j_end]:
                    result.append({**left_row, **right_row})
            i, j = i_end, j_end
    return result
