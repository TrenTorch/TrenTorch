def unfused_memory_traffic(n_elements: int, n_ops: int, bytes_per_element: int = 4) -> int:
    """
    n_elements: size of the array every op operates on
    n_ops: how many elementwise ops are chained (e.g. relu, then scale,
        then add a bias -- 3 ops)
    bytes_per_element: dtype size (4 for float32)

    Running each op as its own separate pass means: op 1 reads the
    original input and writes its own output array; op 2 reads THAT
    output and writes its own new output; and so on. Every op, without
    exception, does one full read and one full write of an
    n_elements-sized array.

    Returns the total bytes moved to/from memory across all n_ops
    separate passes.
    """
    # TODO: each of the n_ops passes reads n_elements and writes
    # n_elements, at bytes_per_element bytes each -- total bytes per
    # pass is 2 * n_elements * bytes_per_element, times n_ops passes.
    pass


def fused_memory_traffic(n_elements: int, bytes_per_element: int = 4) -> int:
    """
    A FUSED kernel computes every chained op's math for one element
    while that element is already sitting in a fast on-chip register --
    it never writes an intermediate result back out to (slow) main
    memory and reads it back in, no matter how many ops are chained
    inside the fused kernel.

    Returns the total bytes moved: read the original input once, write
    the final output once -- regardless of how many ops were fused
    inside.
    """
    # TODO: exactly one read and one write of an n_elements array, at
    # bytes_per_element bytes each.
    pass


def fusion_speedup_estimate(n_elements: int, n_ops: int, bytes_per_element: int = 4) -> float:
    """
    Returns unfused_memory_traffic / fused_memory_traffic -- how many
    times more memory traffic the unfused version costs, for the same
    computation.
    """
    # TODO: call both functions above and divide.
    pass
