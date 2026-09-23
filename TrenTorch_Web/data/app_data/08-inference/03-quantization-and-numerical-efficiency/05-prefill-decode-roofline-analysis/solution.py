def _analyze(flops, bytes_moved, peak_flops_per_sec, peak_bytes_per_sec):
    compute_time = flops / peak_flops_per_sec
    memory_time = bytes_moved / peak_bytes_per_sec if bytes_moved > 0 else 0.0
    intensity = (flops / bytes_moved) if bytes_moved > 0 else float("inf")
    ridge_point = peak_flops_per_sec / peak_bytes_per_sec

    predicted_time = max(compute_time, memory_time)
    bound = "compute_bound" if compute_time >= memory_time else "memory_bound"

    return {
        "arithmetic_intensity": intensity,
        "ridge_point": ridge_point,
        "compute_time_s": compute_time,
        "memory_time_s": memory_time,
        "predicted_time_s": predicted_time,
        "classification": bound,
    }


def roofline_analysis(
    peak_flops_per_sec: float,
    peak_bytes_per_sec: float,
    prefill_flops: float,
    prefill_bytes: float,
    decode_flops: float,
    decode_bytes: float,
) -> dict:
    return {
        "prefill": _analyze(prefill_flops, prefill_bytes, peak_flops_per_sec, peak_bytes_per_sec),
        "decode": _analyze(decode_flops, decode_bytes, peak_flops_per_sec, peak_bytes_per_sec),
    }
