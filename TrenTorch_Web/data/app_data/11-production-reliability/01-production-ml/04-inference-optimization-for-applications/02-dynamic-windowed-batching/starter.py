def batch_requests(
    requests: list[tuple[float, str]], max_batch_size: int, max_wait_ms: float
) -> list[list[str]]:
    """Each request is (arrival_time_ms, request_id), sorted by arrival
    time. Group requests into batches: a batch starts with the first
    request that opens it, and keeps accepting the next request as long as
    the batch isn't already at `max_batch_size` AND that next request
    arrived within `max_wait_ms` of the batch's first request. The moment
    either limit would be exceeded, close the current batch and start a new
    one with that request. Return the list of batches, each a list of
    request ids in arrival order.
    """
    # TODO: implement
    pass
