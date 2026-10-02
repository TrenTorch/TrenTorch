def nested_loop_join(left: list, right: list, key: str) -> list:
    """
    Inner join on left[key] == right[key]. Each output row is
    {**left_row, **right_row} (right wins on a name clash). Output is in
    left-table order, and for each left row its matches in right-table
    order.
    """
    # TODO: Compare every left row with every right row.
    pass


def hash_join(left: list, right: list, key: str) -> list:
    """
    Same result and order as nested_loop_join, but build a dict from key
    to the list of right rows (in right-table order) and probe it once
    per left row. Do not compare every pair.
    """
    # TODO: Build a hash table on the right side, then probe with the left.
    pass


def sort_merge_join(left: list, right: list, key: str) -> list:
    """
    Same rows as the other joins, ordered by key ascending, then by left
    order, then by right order. Stably sort each side once by key, then
    advance two positions through them. Do not compare every pair.
    """
    # TODO: Sort both sides and merge, emitting runs of equal keys.
    pass
