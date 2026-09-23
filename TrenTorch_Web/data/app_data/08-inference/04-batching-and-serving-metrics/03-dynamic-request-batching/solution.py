def dynamic_request_batching(max_batch_size: int, max_wait_time: float, arrivals: list) -> dict:
    batches = []
    current_batch: list = []
    current_start = None

    for arrival_time, req_id in arrivals:
        if current_batch and arrival_time >= current_start + max_wait_time:
            batches.append({"requests": current_batch, "close_time": current_start + max_wait_time})
            current_batch, current_start = [], None

        if not current_batch:
            current_start = arrival_time
        current_batch.append(req_id)

        if len(current_batch) == max_batch_size:
            batches.append({"requests": current_batch, "close_time": arrival_time})
            current_batch, current_start = [], None

    if current_batch:
        batches.append({"requests": current_batch, "close_time": current_start + max_wait_time})

    return {
        "batches": [b["requests"] for b in batches],
        "close_times": [b["close_time"] for b in batches],
    }
