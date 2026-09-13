import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

unfused_memory_traffic = load_solution("08-systems-performance/06-kernels/01-kernel-fusion").unfused_memory_traffic
fused_memory_traffic = load_solution("08-systems-performance/06-kernels/01-kernel-fusion").fused_memory_traffic


def eager_mode_traffic(n_elements: int, n_ops: int, bytes_per_element: int = 4) -> int:
    """
    Eager mode (PyTorch's default): each op in a chain of n_ops
    operations runs, and finishes completely, the instant Python
    reaches that line -- exactly 01-kernel-fusion's "unfused" case,
    since nothing has a chance to look ahead and fuse anything.
    """
    # TODO: this is exactly 01-kernel-fusion's unfused_memory_traffic,
    # reused directly.
    pass


def compiled_graph_traffic(n_elements: int, n_ops: int, bytes_per_element: int = 4) -> int:
    """
    torch.compile traces the WHOLE chain of ops into one graph first,
    then hands that graph to a compiler (TorchInductor) that can fuse
    the pointwise ops in it into a single kernel -- exactly
    01-kernel-fusion's "fused" case. Takes the same (n_elements, n_ops,
    bytes_per_element) signature as eager_mode_traffic for a fair,
    apples-to-apples comparison, even though the fused result doesn't
    actually depend on n_ops.
    """
    # TODO: this is exactly 01-kernel-fusion's fused_memory_traffic
    # (n_ops isn't used inside it -- that's the whole point).
    pass


def compiled_speedup_estimate(n_elements: int, n_ops: int, bytes_per_element: int = 4) -> float:
    """
    Returns eager_mode_traffic / compiled_graph_traffic -- how much
    memory-traffic overhead compiling the whole chain into one fused
    graph eliminates, compared to running it eagerly, op by op.
    """
    # TODO: call both functions above and divide.
    pass
