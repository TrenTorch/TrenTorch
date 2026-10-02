def running_sum(values: list, partitions: list) -> list:
    """
    Entry i is the sum of values[j] over rows j <= i that have the same
    partition as row i. Rows are in window order.
    """
    # TODO: Keep one running total per partition.
    pass


def rank(values: list, partitions: list) -> list:
    """
    Entry i is 1 + the number of rows in the same partition with a
    strictly larger value. Ties share a rank and the next rank is
    skipped (9, 9, 7 -> 1, 1, 3).
    """
    # TODO: Count the larger values in the same partition.
    pass


def lag(values: list, partitions: list, offset: int, default=None) -> list:
    """
    Entry i is the value `offset` rows earlier within the same partition
    (offset >= 1), or `default` if there is no such row.
    """
    # TODO: Remember the values seen so far in each partition.
    pass


def moving_average(values: list, window: int) -> list:
    """
    Entry i is the mean of values[max(0, i - window + 1) : i + 1] as a
    float, so early entries average over fewer values. Ignores
    partitions. window >= 1.
    """
    # TODO: Average the trailing window at each position.
    pass
