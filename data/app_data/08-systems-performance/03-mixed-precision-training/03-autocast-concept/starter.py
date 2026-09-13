_FP16_SAFE_OPS = {"matmul", "linear", "conv2d", "relu"}
_FP32_REQUIRED_OPS = {"softmax", "log_softmax", "layer_norm", "batch_norm", "cross_entropy", "sum", "mean", "exp", "log"}


def should_run_in_fp16(op_name: str) -> bool:
    """
    op_name: the name of a real neural network operation

    Autocast doesn't run an ENTIRE model in fp16 -- it runs each
    individual op at whichever precision is safe for that op. Matrix
    multiplications and convolutions (dominated by many small
    multiply-adds, tolerant of fp16's reduced precision, and the
    actual bottleneck fp16 speeds up) are safe. Reductions and
    exponentials (summing many values, or exponentiating a large
    range of numbers, as softmax/layer_norm/batch_norm do internally)
    are numerically fragile in fp16 and need fp32's extra range and
    precision to stay stable.

    Raises ValueError for any op_name not in either known list.
    """
    # TODO: return False if op_name is in _FP32_REQUIRED_OPS, True if
    # it's in _FP16_SAFE_OPS, otherwise raise ValueError.
    pass


def autocast_dtype_for(op_name: str) -> str:
    """
    Returns "float16" or "float32", whichever should_run_in_fp16 says
    this op should actually run at.
    """
    # TODO: one line, built directly on should_run_in_fp16.
    pass
