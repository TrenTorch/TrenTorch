PARAM_BYTES_FP16 = 2
GRAD_BYTES_FP16 = 2
ADAM_OPTIMIZER_STATE_MULTIPLIER = 12


def per_gpu_memory_bytes(num_params: int, num_gpus: int, zero_stage: int) -> float:
    k = ADAM_OPTIMIZER_STATE_MULTIPLIER
    if zero_stage == 0:
        return (PARAM_BYTES_FP16 + GRAD_BYTES_FP16 + k) * num_params
    if zero_stage == 1:
        return (PARAM_BYTES_FP16 + GRAD_BYTES_FP16) * num_params + k * num_params / num_gpus
    if zero_stage == 2:
        return PARAM_BYTES_FP16 * num_params + (GRAD_BYTES_FP16 + k) * num_params / num_gpus
    if zero_stage == 3:
        return (PARAM_BYTES_FP16 + GRAD_BYTES_FP16 + k) * num_params / num_gpus
    raise ValueError(f"zero_stage must be 0-3, got {zero_stage}")


def memory_reduction_factor(num_params: int, num_gpus: int, zero_stage: int) -> float:
    baseline = per_gpu_memory_bytes(num_params, num_gpus, zero_stage=0)
    sharded = per_gpu_memory_bytes(num_params, num_gpus, zero_stage)
    return baseline / sharded
