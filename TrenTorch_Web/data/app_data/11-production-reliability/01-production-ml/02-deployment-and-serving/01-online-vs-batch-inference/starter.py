import math


def online_inference(model_fn, request):
    """
    Online (request-by-request) inference: handle ONE request the
    moment it arrives, calling the model on a batch of size 1 and
    returning immediately -- lowest possible latency for that one
    request, but pays the model's fixed per-call overhead every
    single time.
    """
    # TODO: return model_fn([request])[0]
    pass


def batch_inference(model_fn, requests: list) -> list:
    """
    Batch inference: process MANY requests together in one model
    call, amortizing the fixed per-call overhead across all of them
    -- higher throughput, but no single request gets a result until
    the whole batch is ready to go.
    """
    # TODO: return model_fn(requests)
    pass


def online_total_overhead(num_requests: int, overhead_per_call: float) -> float:
    """
    Total fixed overhead paid across num_requests SEPARATE online
    calls -- one overhead charge per request.
    """
    # TODO: num_requests * overhead_per_call
    pass


def batch_total_overhead(num_requests: int, overhead_per_call: float, batch_size: int) -> float:
    """
    Total fixed overhead paid when the same num_requests are grouped
    into batches of batch_size -- one overhead charge PER BATCH
    (rounding up: a partially-full final batch still costs a full
    overhead charge).
    """
    # TODO: math.ceil(num_requests / batch_size) * overhead_per_call
    pass


def worst_case_batch_wait_time(batch_size: int, per_request_arrival_interval: float) -> float:
    """
    The longest a single request might sit waiting for its batch to
    fill up: the FIRST request into an empty batch has to wait for
    (batch_size - 1) MORE requests to arrive (each taking, on
    average, per_request_arrival_interval) before the batch actually
    runs.
    """
    # TODO: (batch_size - 1) * per_request_arrival_interval
    pass
