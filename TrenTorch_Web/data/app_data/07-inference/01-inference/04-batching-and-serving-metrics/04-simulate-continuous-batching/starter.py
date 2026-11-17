def simulate_continuous_batching(max_batch_size: int, requests: list) -> dict:
    """
    requests: list of [arrival_step, request_id, n_tokens_needed].

    Returns a dict with keys "admitted_step" (request_id -> step),
    "finished_step" (request_id -> step), and "total_steps".
    """
    # TODO: At each step, decrement every active request's remaining
    # tokens, evict finished ones, THEN admit from the FIFO wait queue
    # to refill up to max_batch_size. Evict before admit, same step.
    # See Theory hint.
    pass
