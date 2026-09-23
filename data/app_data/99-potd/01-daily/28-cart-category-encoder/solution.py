def encode_departments(departments: list[str]) -> tuple[list[str], list[list[int]]]:
    distinct = sorted(set(departments))
    index_of = {dept: i for i, dept in enumerate(distinct)}
    k = len(distinct)

    rows = []
    for dept in departments:
        row = [0] * k
        row[index_of[dept]] = 1
        rows.append(row)

    return distinct, rows
