def arithmetic_intensity(flops: int, bytes_moved: int) -> float:
    return flops / bytes_moved


def ridge_point(peak_flops_per_sec: float, peak_bytes_per_sec: float) -> float:
    return peak_flops_per_sec / peak_bytes_per_sec


def is_memory_bound(
    flops: int, bytes_moved: int, peak_flops_per_sec: float, peak_bytes_per_sec: float
) -> bool:
    ai = arithmetic_intensity(flops, bytes_moved)
    rp = ridge_point(peak_flops_per_sec, peak_bytes_per_sec)
    return ai < rp


def achievable_flops_per_sec(
    flops: int, bytes_moved: int, peak_flops_per_sec: float, peak_bytes_per_sec: float
) -> float:
    ai = arithmetic_intensity(flops, bytes_moved)
    return min(peak_flops_per_sec, ai * peak_bytes_per_sec)
