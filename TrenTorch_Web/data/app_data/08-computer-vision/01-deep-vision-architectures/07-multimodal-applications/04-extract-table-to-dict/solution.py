def rows_to_records(header: list[str], rows: list[list[str]]) -> list[dict]:
    records = []
    for row in rows:
        record = dict(zip(header, row))
        records.append(record)
    return records
