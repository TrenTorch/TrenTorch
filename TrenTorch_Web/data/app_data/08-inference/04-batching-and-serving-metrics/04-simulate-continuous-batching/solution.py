def simulate_continuous_batching(max_batch_size: int, requests: list) -> dict:
    by_arrival = sorted(requests, key=lambda r: r[0])
    queue = list(by_arrival)
    active: dict = {}
    admitted_step: dict = {}
    finished_step: dict = {}
    step = 0

    def admit_arrivals_and_fill():
        nonlocal queue
        still_waiting = []
        for arrival_step, rid, need in queue:
            if arrival_step <= step and len(active) < max_batch_size:
                active[rid] = need
                admitted_step[rid] = step
            else:
                still_waiting.append((arrival_step, rid, need))
        queue = still_waiting

    admit_arrivals_and_fill()

    while active or queue:
        if not active and queue:
            step = queue[0][0]
            admit_arrivals_and_fill()
            continue

        for rid in list(active):
            active[rid] -= 1
            if active[rid] == 0:
                finished_step[rid] = step
                del active[rid]

        step += 1
        admit_arrivals_and_fill()

    return {"admitted_step": admitted_step, "finished_step": finished_step, "total_steps": step}
