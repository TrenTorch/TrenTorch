import numpy as np


def serving_metrics(request_arrival_time: float, token_timestamps: list) -> dict:
    """
    request_arrival_time: when the request arrived.
    token_timestamps: strictly increasing timestamps, one per generated
    token, all >= request_arrival_time.

    Returns a dict with keys "ttft", "itl" (list), "tpot" (None if <2
    tokens), and "throughput_tokens_per_sec".
    """
    # TODO: TTFT = first timestamp - arrival. ITL = consecutive gaps.
    # TPOT = mean(ITL), or None if fewer than 2 tokens. Throughput =
    # n_tokens / (last timestamp - arrival).
    pass
