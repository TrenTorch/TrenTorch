PARAM_BYTES_FP16 = 2
GRAD_BYTES_FP16 = 2
ADAM_OPTIMIZER_STATE_MULTIPLIER = 12


def per_gpu_memory_bytes(num_params: int, num_gpus: int, zero_stage: int) -> float:
    """
    Per-GPU memory (in bytes-per-parameter units), following the ZeRO
    paper's mixed-precision Adam model: fp16 params (2 bytes/param),
    fp16 grads (2 bytes/param), and fp32 Adam optimizer state
    (K=12 bytes/param: fp32 param copy + momentum + variance).

    zero_stage 0: no sharding at all -- every GPU holds everything:
        (2 + 2 + K) * num_params
    zero_stage 1 (P_os): shard ONLY optimizer state across num_gpus:
        (2 + 2) * num_params + K * num_params / num_gpus
    zero_stage 2 (P_os+g): also shard gradients:
        2 * num_params + (2 + K) * num_params / num_gpus
    zero_stage 3 (P_os+g+p): also shard parameters -- everything sharded:
        (2 + 2 + K) * num_params / num_gpus
    """
    # TODO: implement the four cases above; raise ValueError for any
    # other zero_stage.
    pass


def memory_reduction_factor(num_params: int, num_gpus: int, zero_stage: int) -> float:
    """
    How many times less per-GPU memory a given ZeRO stage uses,
    compared to zero_stage 0 (no sharding at all).
    """
    # TODO: per_gpu_memory_bytes(..., zero_stage=0) / per_gpu_memory_bytes(..., zero_stage)
    pass
