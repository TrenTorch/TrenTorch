def bytes_per_param(zero_stage: int, n_gpus: int) -> float:
    """Bytes per parameter on one GPU: weights 2, grads 2, optimizer 12, sharded by ZeRO stage."""
    # TODO
    pass


def training_memory_gib(n_params: float, zero_stage: int, n_gpus: int) -> float:
    """Per-GPU memory in GiB for parameters, gradients and optimizer state."""
    # TODO
    pass
