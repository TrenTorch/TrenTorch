def top_characters(s, k):
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    items = [[ch, n] for ch, n in counts.items()]
    for i in range(1, len(items)):
        j = i
        while j > 0 and (
            items[j][1] > items[j - 1][1]
            or (items[j][1] == items[j - 1][1] and items[j][0] < items[j - 1][0])
        ):
            items[j], items[j - 1] = items[j - 1], items[j]
            j -= 1
    return items[:k]
