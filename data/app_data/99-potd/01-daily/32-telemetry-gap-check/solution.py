def count_missing_per_column(columns: list[str], rows: list[list[str]]) -> list[int]:
    counts = [0] * len(columns)
    for row in rows:
        for j, value in enumerate(row):
            if value == "NA":
                counts[j] += 1
    return counts
