def dynamic_request_batching(max_batch_size: int, max_wait_time: float, arrivals: list) -> dict:
    """
    arrivals: list of (arrival_time, request_id) tuples, sorted by
    arrival_time.

    Returns a dict with keys "batches" (list of lists of request ids)
    and "close_times" (one close time per batch).
    """
    # TODO: Track the current open batch's start time. A request either
    # joins the current batch (if not full and not timed out) or starts
    # a new one. Close a batch immediately when it reaches
    # max_batch_size, or when the next arrival is at/after
    # batch_start + max_wait_time. See Theory hint.
    pass
