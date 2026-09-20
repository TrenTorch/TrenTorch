def batch_requests(
    requests: list[tuple[float, str]], max_batch_size: int, max_wait_ms: float
) -> list[list[str]]:
    batches: list[list[str]] = []
    current_batch: list[str] = []
    batch_start_time = None
    for arrival_time, request_id in requests:
        if not current_batch:
            current_batch = [request_id]
            batch_start_time = arrival_time
            continue
        if len(current_batch) >= max_batch_size or (arrival_time - batch_start_time) > max_wait_ms:
            batches.append(current_batch)
            current_batch = [request_id]
            batch_start_time = arrival_time
        else:
            current_batch.append(request_id)
    if current_batch:
        batches.append(current_batch)
    return batches
