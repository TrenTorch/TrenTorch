def scan(table: list):
    for row in table:
        yield row


def filter_rows(rows, predicate):
    for row in rows:
        if predicate(row):
            yield row


def project(rows, columns: list):
    for row in rows:
        yield {column: row[column] for column in columns}


def order_by(rows, column: str, descending: bool = False):
    collected = list(rows)
    present = [row for row in collected if row[column] is not None]
    missing = [row for row in collected if row[column] is None]
    for row in sorted(present, key=lambda r: r[column], reverse=descending):
        yield row
    for row in missing:
        yield row


def limit(rows, n: int):
    if n <= 0:
        return
    produced = 0
    for row in rows:
        yield row
        produced += 1
        if produced >= n:
            return


def run_query(table: list, where=None, columns=None, order_column=None, descending: bool = False, row_limit=None) -> list:
    stream = scan(table)
    if where is not None:
        stream = filter_rows(stream, where)
    if order_column is not None:
        stream = order_by(stream, order_column, descending)
    if row_limit is not None:
        stream = limit(stream, row_limit)
    if columns is not None:
        stream = project(stream, columns)
    return list(stream)
