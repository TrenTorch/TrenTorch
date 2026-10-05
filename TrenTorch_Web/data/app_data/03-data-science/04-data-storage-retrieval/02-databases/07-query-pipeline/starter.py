def scan(table: list):
    """A generator: yields the rows of the list in order."""
    # TODO: Yield each row.
    pass


def filter_rows(rows, predicate):
    """A generator: yields only the rows for which predicate(row) is true."""
    # TODO: Pull rows one at a time and yield the ones that pass.
    pass


def project(rows, columns: list):
    """
    A generator: yields a NEW dict per row with only `columns`, in the
    order listed.
    """
    # TODO: Build the narrowed row for each input row.
    pass


def order_by(rows, column: str, descending: bool = False):
    """
    A blocking operator: reads ALL input first, then yields the rows
    sorted by row[column] (stable, also when descending). Rows whose
    value is None come last in both directions.
    """
    # TODO: Collect the rows, sort them, then yield them.
    pass


def limit(rows, n: int):
    """
    A generator: yields at most n rows and stops WITHOUT pulling another
    row from its input once n have been yielded (n <= 0 pulls none).
    """
    # TODO: Count what you yield and stop as soon as you reach n.
    pass


def run_query(table: list, where=None, columns=None, order_column=None, descending: bool = False, row_limit=None) -> list:
    """
    Returns a list. Order of steps: scan, filter (if where is not None),
    sort (if order_column is not None), limit (if row_limit is not None),
    project (if columns is not None).
    """
    # TODO: Chain the operators in the order above.
    pass
