def dedupe_idempotent_calls(call_ids: list[str]) -> list[tuple[str, bool]]:
    """
    call_ids: the idempotency key for every attempted tool call, in
    order (a retry of the same logical call reuses the same key).

    For each call, decide whether it should actually EXECUTE (True,
    the first time this exact key is seen) or be treated as a no-op
    that reuses the earlier result (False, every later occurrence of
    an already-seen key).

    Returns (call_id, executed) pairs, in the original order.
    """
    # TODO: Implement the idempotency-key dedup from Theory.
    pass
