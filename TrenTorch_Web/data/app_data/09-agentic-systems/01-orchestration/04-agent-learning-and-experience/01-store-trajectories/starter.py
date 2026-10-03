def classify_and_store(trajectories: list[tuple[str, bool]]) -> tuple[list[str], list[str]]:
    """
    trajectories: (trajectory_id, success) pairs, in order.

    Split them into two lists: ids of successful trajectories and ids
    of failed ones, each preserving the original relative order.

    Returns (successful_ids, failed_ids).
    """
    # TODO: Implement the partition from Theory.
    pass
