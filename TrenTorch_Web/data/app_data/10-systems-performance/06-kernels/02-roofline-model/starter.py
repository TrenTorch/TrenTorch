def arithmetic_intensity(flops: int, bytes_moved: int) -> float:
    """
    flops: total floating-point operations a computation performs
    bytes_moved: total bytes read from and written to memory

    Arithmetic intensity: how much computation is done per byte of
    memory traffic. High intensity means lots of math per byte fetched
    (compute has plenty to do while waiting on memory); low intensity
    means the hardware spends most of its time waiting for data it can
    barely keep up with feeding to the compute units.
    """
    # TODO: flops / bytes_moved.
    pass


def ridge_point(peak_flops_per_sec: float, peak_bytes_per_sec: float) -> float:
    """
    peak_flops_per_sec: the hardware's maximum possible compute throughput
    peak_bytes_per_sec: the hardware's maximum possible memory bandwidth

    The ridge point is the arithmetic intensity at which a computation
    exactly saturates BOTH compute and memory bandwidth at the same
    time -- below it, memory bandwidth is the bottleneck; above it,
    compute is.
    """
    # TODO: peak_flops_per_sec / peak_bytes_per_sec.
    pass


def is_memory_bound(
    flops: int, bytes_moved: int, peak_flops_per_sec: float, peak_bytes_per_sec: float
) -> bool:
    """
    Returns True if this computation's own arithmetic intensity falls
    below the hardware's ridge point (memory bandwidth is the
    bottleneck), False if it's at or above it (compute is the
    bottleneck).
    """
    # TODO: compare arithmetic_intensity(...) against ridge_point(...).
    pass


def achievable_flops_per_sec(
    flops: int, bytes_moved: int, peak_flops_per_sec: float, peak_bytes_per_sec: float
) -> float:
    """
    The roofline model's central prediction: the actual achievable
    throughput for a computation with this arithmetic intensity, given
    this hardware's peak compute and peak memory bandwidth.

    Below the ridge point, throughput is capped by how fast data can
    arrive (intensity * bandwidth). At or above the ridge point,
    throughput is capped by the hardware's raw compute ceiling,
    regardless of how much MORE intense the computation gets.
    """
    # TODO: min(peak_flops_per_sec, arithmetic_intensity(flops,
    # bytes_moved) * peak_bytes_per_sec).
    pass
