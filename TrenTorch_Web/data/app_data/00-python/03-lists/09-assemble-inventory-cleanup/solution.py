import copy


def label_of(row: list) -> str:
    return row[0]


def quantity_of(row: list) -> int:
    return row[1]


def process_inventory(rows: list, min_qty: int) -> list:
    snapshot = copy.deepcopy(rows)

    kept = [row for row in rows if quantity_of(row) >= min_qty]
    rows[:] = kept

    rows.sort(key=label_of)
    rows.sort(key=quantity_of, reverse=True)

    top_labels = [label_of(row) for row in rows[:3]]
    quantities = [quantity_of(row) for row in rows]

    return [snapshot, top_labels, quantities]
