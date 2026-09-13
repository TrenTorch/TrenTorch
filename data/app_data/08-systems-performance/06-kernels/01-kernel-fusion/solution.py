def unfused_memory_traffic(n_elements: int, n_ops: int, bytes_per_element: int = 4) -> int:
    return n_ops * 2 * n_elements * bytes_per_element


def fused_memory_traffic(n_elements: int, bytes_per_element: int = 4) -> int:
    return 2 * n_elements * bytes_per_element


def fusion_speedup_estimate(n_elements: int, n_ops: int, bytes_per_element: int = 4) -> float:
    unfused = unfused_memory_traffic(n_elements, n_ops, bytes_per_element)
    fused = fused_memory_traffic(n_elements, bytes_per_element)
    return unfused / fused
