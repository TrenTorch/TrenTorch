import numpy as np


def serving_metrics(request_arrival_time: float, token_timestamps: list) -> dict:
    ts = np.array(token_timestamps, dtype=float)
    n = len(ts)

    ttft = float(ts[0] - request_arrival_time)
    itl = (ts[1:] - ts[:-1]).tolist() if n > 1 else []
    tpot = float(np.mean(itl)) if itl else None
    total_time = ts[-1] - request_arrival_time
    throughput = n / total_time if total_time > 0 else float("inf")

    return {"ttft": ttft, "itl": itl, "tpot": tpot, "throughput_tokens_per_sec": throughput}
