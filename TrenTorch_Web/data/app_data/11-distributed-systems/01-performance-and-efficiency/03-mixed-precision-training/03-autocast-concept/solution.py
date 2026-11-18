_FP16_SAFE_OPS = {"matmul", "linear", "conv2d", "relu"}
_FP32_REQUIRED_OPS = {"softmax", "log_softmax", "layer_norm", "batch_norm", "cross_entropy", "sum", "mean", "exp", "log"}


def should_run_in_fp16(op_name: str) -> bool:
    if op_name in _FP32_REQUIRED_OPS:
        return False
    if op_name in _FP16_SAFE_OPS:
        return True
    raise ValueError(f"Unknown op: {op_name!r}")


def autocast_dtype_for(op_name: str) -> str:
    return "float16" if should_run_in_fp16(op_name) else "float32"
