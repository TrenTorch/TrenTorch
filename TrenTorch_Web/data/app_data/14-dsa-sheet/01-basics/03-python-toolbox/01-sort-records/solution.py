def sort_records(records):
    return [name for name, _ in sorted(records, key=lambda r: (-r[1], r[0]))]
