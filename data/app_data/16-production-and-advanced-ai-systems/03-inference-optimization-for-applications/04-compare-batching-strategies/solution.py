import math


def compare_batching_strategies(
    num_requests: int,
    max_batch_size: int,
    per_request_ms: float,
    per_batch_overhead_ms: float,
) -> dict:
    individual_total_ms = num_requests * (per_request_ms + per_batch_overhead_ms)
    num_batches = math.ceil(num_requests / max_batch_size) if num_requests > 0 else 0
    batched_total_ms = num_requests * per_request_ms + num_batches * per_batch_overhead_ms
    return {
        "individual_total_ms": individual_total_ms,
        "batched_total_ms": batched_total_ms,
        "savings_ms": individual_total_ms - batched_total_ms,
    }
