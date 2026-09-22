def compare_batching_strategies(
    num_requests: int,
    max_batch_size: int,
    per_request_ms: float,
    per_batch_overhead_ms: float,
) -> dict:
    """Compare processing `num_requests` one at a time versus batched in
    groups of up to `max_batch_size`. Each request costs `per_request_ms`
    regardless of strategy; each individual call additionally pays
    `per_batch_overhead_ms` once (its own fixed setup cost), while a batch
    pays that overhead once per batch, shared across every request in it.
    Return a dict with "individual_total_ms", "batched_total_ms", and
    "savings_ms" (individual minus batched).
    """
    # TODO: implement
    pass
