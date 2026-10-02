def _aggregate(values: list, function_name: str, row_count: int):
    if function_name == "count":
        return row_count
    present = [v for v in values if v is not None]
    if function_name not in ("sum", "mean", "min", "max"):
        raise ValueError(f"unknown aggregate {function_name!r}")
    if not present:
        return None
    if function_name == "sum":
        return sum(present)
    if function_name == "mean":
        return sum(present) / len(present)
    if function_name == "min":
        return min(present)
    return max(present)


def group_by(rows: list, keys: list, aggregations: dict) -> list:
    groups = {}
    for row in rows:
        groups.setdefault(tuple(row[k] for k in keys), []).append(row)
    result = []
    for key_values in sorted(groups):
        members = groups[key_values]
        out = dict(zip(keys, key_values))
        for name, (column, function_name) in aggregations.items():
            values = [r[column] for r in members] if function_name != "count" else []
            out[name] = _aggregate(values, function_name, len(members))
        result.append(out)
    return result


def having(groups: list, predicate) -> list:
    return [group for group in groups if predicate(group)]


def count_distinct(rows: list, column: str) -> int:
    return len({row[column] for row in rows if row[column] is not None})
