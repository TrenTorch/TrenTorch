import math


def online_inference(model_fn, request):
    return model_fn([request])[0]


def batch_inference(model_fn, requests: list) -> list:
    return model_fn(requests)


def online_total_overhead(num_requests: int, overhead_per_call: float) -> float:
    return num_requests * overhead_per_call


def batch_total_overhead(num_requests: int, overhead_per_call: float, batch_size: int) -> float:
    num_batches = math.ceil(num_requests / batch_size)
    return num_batches * overhead_per_call


def worst_case_batch_wait_time(batch_size: int, per_request_arrival_interval: float) -> float:
    return (batch_size - 1) * per_request_arrival_interval
