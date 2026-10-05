def group_by(rows: list, keys: list, aggregations: dict) -> list:
    """
    rows: list of dicts
    keys: non-empty list of column names defining the group
    aggregations: {output_name: (column, function_name)} with function_name
        in "count", "sum", "mean", "min", "max"

    Returns a list of dicts, one per distinct tuple of key values, sorted
    ascending by that tuple. Each dict holds the key columns, then the
    aggregates in the order given. Aggregates skip None values; "count"
    counts every row; a group with no non-None values gives None for sum,
    mean, min and max. Unknown function names raise ValueError. An empty
    table returns [].
    """
    # TODO: Split into groups with a dict of key tuples, then aggregate.
    pass


def having(groups: list, predicate) -> list:
    """Returns the groups for which predicate(group) is true, in order."""
    # TODO: Filter the aggregated groups.
    pass


def count_distinct(rows: list, column: str) -> int:
    """Returns the number of different non-None values in `column`."""
    # TODO: Count the unique values.
    pass
