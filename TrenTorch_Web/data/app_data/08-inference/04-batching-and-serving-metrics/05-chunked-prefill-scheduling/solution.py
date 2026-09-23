def chunked_prefill_scheduling(token_budget: int, n_decode_tokens_each: int, requests: list) -> dict:
    by_arrival = sorted(requests, key=lambda r: r[0])
    queue = list(by_arrival)
    prefill_remaining: dict = {}
    decode_remaining: dict = {}
    prefill_done_step: dict = {}
    completed_step: dict = {}
    step = 0
    order: list = []

    def admit_new_arrivals():
        nonlocal queue
        still_waiting = []
        for arrival_step, rid, prefill_tokens in queue:
            if arrival_step <= step:
                prefill_remaining[rid] = prefill_tokens
                order.append(rid)
            else:
                still_waiting.append((arrival_step, rid, prefill_tokens))
        queue = still_waiting

    admit_new_arrivals()

    while prefill_remaining or decode_remaining or queue:
        budget = token_budget
        for rid in list(decode_remaining):
            decode_remaining[rid] -= 1
            budget -= 1
            if decode_remaining[rid] == 0:
                completed_step[rid] = step
                del decode_remaining[rid]

        just_finished_prefill = []
        for rid in list(order):
            if budget <= 0:
                break
            if rid not in prefill_remaining:
                continue
            chunk = min(budget, prefill_remaining[rid])
            prefill_remaining[rid] -= chunk
            budget -= chunk
            if prefill_remaining[rid] == 0:
                prefill_done_step[rid] = step
                just_finished_prefill.append(rid)
                del prefill_remaining[rid]

        for rid in just_finished_prefill:
            order.remove(rid)
            decode_remaining[rid] = n_decode_tokens_each

        step += 1
        admit_new_arrivals()

    return {"prefill_done_step": prefill_done_step, "completed_step": completed_step, "total_steps": step}
