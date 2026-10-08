def zero_memory_per_gpu(psi, N, stage):
    """
    psi: number of model parameters
    N: data-parallel degree (number of GPUs)
    stage: ZeRO stage, 0 (none), 1 (optimizer states), 2 (plus gradients), 3 (plus parameters)

    Returns:
        Bytes per GPU for mixed-precision Adam training: 16 bytes per parameter in total,
        partitioned by stage.
    """
    # TODO: Apply the per-stage partitioning of the 16 bytes per parameter (see Theory).
    pass
