import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

unfused_memory_traffic = load_solution("08-systems-performance/06-kernels/01-kernel-fusion").unfused_memory_traffic
fused_memory_traffic = load_solution("08-systems-performance/06-kernels/01-kernel-fusion").fused_memory_traffic


def eager_mode_traffic(n_elements: int, n_ops: int, bytes_per_element: int = 4) -> int:
    return unfused_memory_traffic(n_elements, n_ops, bytes_per_element)


def compiled_graph_traffic(n_elements: int, n_ops: int, bytes_per_element: int = 4) -> int:
    return fused_memory_traffic(n_elements, bytes_per_element)


def compiled_speedup_estimate(n_elements: int, n_ops: int, bytes_per_element: int = 4) -> float:
    eager = eager_mode_traffic(n_elements, n_ops, bytes_per_element)
    compiled = compiled_graph_traffic(n_elements, n_ops, bytes_per_element)
    return eager / compiled
