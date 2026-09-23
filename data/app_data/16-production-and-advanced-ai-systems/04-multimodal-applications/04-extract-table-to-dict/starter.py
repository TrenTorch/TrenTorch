def rows_to_records(header: list[str], rows: list[list[str]]) -> list[dict]:
    """Given a table's header row and its data rows, return one dict per
    row, mapping each header column name to that row's value at the same
    position. If a row has fewer cells than the header, the missing
    trailing columns are simply absent from that row's dict (not filled
    with None or an empty string). Extra trailing cells beyond the header's
    length are dropped.
    """
    # TODO: implement
    pass
