def rows_to_columns(rows: list) -> dict:
    if not rows:
        return {}
    return {name: [row[name] for row in rows] for name in rows[0]}


def columns_to_rows(columns: dict) -> list:
    if not columns:
        return []
    names = list(columns)
    return [dict(zip(names, values)) for values in zip(*(columns[name] for name in names))]


def run_length_encode(values: list) -> list:
    pairs = []
    for value in values:
        if pairs and pairs[-1][0] == value:
            pairs[-1] = (value, pairs[-1][1] + 1)
        else:
            pairs.append((value, 1))
    return pairs


def run_length_decode(pairs: list) -> list:
    values = []
    for value, count in pairs:
        values.extend([value] * count)
    return values


def bytes_scanned(layout: str, num_rows: int, num_columns: int, columns_needed: int, value_bytes: int) -> int:
    if layout == "row":
        return int(num_rows * num_columns * value_bytes)
    if layout == "column":
        return int(num_rows * columns_needed * value_bytes)
    raise ValueError(f"unknown layout {layout!r}")
