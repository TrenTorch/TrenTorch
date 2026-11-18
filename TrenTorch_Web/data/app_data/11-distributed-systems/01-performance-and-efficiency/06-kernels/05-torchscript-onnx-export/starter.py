def eager_python_dispatch_overhead(num_ops: int, per_op_dispatch_seconds: float) -> float:
    """
    num_ops: how many individual tensor operations a model's forward
        pass calls
    per_op_dispatch_seconds: the fixed Python-interpreter + framework
        overhead of dispatching ONE op call (deciding which C++/CUDA
        kernel to actually run, checking types/devices, etc.) -- real
        and measurable, separate from the actual math the op performs

    In eager mode, every single op the forward pass calls pays this
    dispatch overhead separately, one Python function call at a time --
    05-acceleration's "per-iteration Python cost" lesson, applied to
    framework op dispatch instead of a raw arithmetic loop.
    """
    # TODO: num_ops * per_op_dispatch_seconds.
    pass


def graph_mode_dispatch_overhead(per_op_dispatch_seconds: float) -> float:
    """
    A compiled/exported graph (TorchScript, ONNX) is executed as ONE
    call into a runtime that then runs the whole graph natively --
    Python dispatches the request exactly once, regardless of how many
    ops the graph actually contains internally.
    """
    # TODO: just per_op_dispatch_seconds -- paid exactly once, no
    # multiplication by num_ops at all.
    pass


def graph_mode_speedup_estimate(num_ops: int, per_op_dispatch_seconds: float) -> float:
    """
    Returns eager_python_dispatch_overhead / graph_mode_dispatch_overhead
    -- how many times more DISPATCH overhead (not compute -- purely the
    Python/framework bookkeeping cost) eager mode pays compared to
    running the same ops as one compiled graph.
    """
    # TODO: call both functions above and divide.
    pass
