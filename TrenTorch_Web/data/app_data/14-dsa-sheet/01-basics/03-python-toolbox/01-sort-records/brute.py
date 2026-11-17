def sort_records(records):
    items = [list(r) for r in records]
    for i in range(1, len(items)):
        j = i
        while j > 0 and (
            items[j][1] > items[j - 1][1]
            or (items[j][1] == items[j - 1][1] and items[j][0] < items[j - 1][0])
        ):
            items[j], items[j - 1] = items[j - 1], items[j]
            j -= 1
    return [r[0] for r in items]
