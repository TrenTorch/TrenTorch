def eager_python_dispatch_overhead(num_ops: int, per_op_dispatch_seconds: float) -> float:
    return num_ops * per_op_dispatch_seconds


def graph_mode_dispatch_overhead(per_op_dispatch_seconds: float) -> float:
    return per_op_dispatch_seconds


def graph_mode_speedup_estimate(num_ops: int, per_op_dispatch_seconds: float) -> float:
    eager = eager_python_dispatch_overhead(num_ops, per_op_dispatch_seconds)
    graph = graph_mode_dispatch_overhead(per_op_dispatch_seconds)
    return eager / graph
