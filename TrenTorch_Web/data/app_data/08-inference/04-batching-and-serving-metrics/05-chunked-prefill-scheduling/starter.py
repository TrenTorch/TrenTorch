def chunked_prefill_scheduling(token_budget: int, n_decode_tokens_each: int, requests: list) -> dict:
    """
    requests: list of [arrival_step, request_id, prefill_tokens].

    Returns a dict with keys "prefill_done_step", "completed_step"
    (both request_id -> step), and "total_steps".
    """
    # TODO: Every step, give 1 token-unit of budget to each active
    # decode-phase request first, then spend the rest on prefill chunks
    # in FIFO order. A prefill that reaches 0 starts decoding NEXT step.
    # See Theory for the exact priority order.
    pass
