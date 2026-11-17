def roofline_analysis(
    peak_flops_per_sec: float,
    peak_bytes_per_sec: float,
    prefill_flops: float,
    prefill_bytes: float,
    decode_flops: float,
    decode_bytes: float,
) -> dict:
    """
    Returns a dict with keys "prefill" and "decode", each a dict with
    "arithmetic_intensity", "ridge_point", "compute_time_s",
    "memory_time_s", "predicted_time_s", "classification".
    """
    # TODO: For prefill and decode independently, compute compute_time =
    # flops/peak_flops_per_sec, memory_time = bytes/peak_bytes_per_sec
    # (0 if bytes_moved is 0), predicted_time = max of the two, and
    # classify by which one is larger. See Theory for the full formula.
    pass
