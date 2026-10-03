def rows_to_columns(rows: list) -> dict:
    """
    rows: list of dicts with the same keys in the same order.
    Returns {column_name: list of that column's values in row order},
    columns in key order. An empty list gives {}.
    """
    # TODO: Transpose the rows into one list per column.
    pass


def columns_to_rows(columns: dict) -> list:
    """
    Inverse of rows_to_columns: returns a list of row dicts with keys in
    the order of `columns`. An empty table gives [].
    """
    # TODO: Zip the columns back into records.
    pass


def run_length_encode(values: list) -> list:
    """
    Returns a list of (value, count) pairs, one per run of equal
    consecutive values, in order. An empty list gives [].
    """
    # TODO: Collapse each run of equal neighbours into one pair.
    pass


def run_length_decode(pairs: list) -> list:
    """Returns the original list from (value, count) pairs."""
    # TODO: Repeat each value by its count.
    pass


def bytes_scanned(layout: str, num_rows: int, num_columns: int, columns_needed: int, value_bytes: int) -> int:
    """
    "row": every value of every row must be read:
        num_rows * num_columns * value_bytes.
    "column": only the needed columns are read:
        num_rows * columns_needed * value_bytes.
    Any other layout raises ValueError.
    """
    # TODO: Apply the cost model from Theory.
    pass
