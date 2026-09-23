def one_hot_encode(categories: list[str]) -> tuple[list[str], list[list[int]]]:
    distinct = sorted(set(categories))
    index_of = {category: i for i, category in enumerate(distinct)}
    k = len(distinct)

    rows = []
    for category in categories:
        row = [0] * k
        row[index_of[category]] = 1
        rows.append(row)

    return distinct, rows
