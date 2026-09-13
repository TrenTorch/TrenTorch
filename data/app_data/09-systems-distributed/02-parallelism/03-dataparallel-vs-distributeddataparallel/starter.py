def dp_communication_volume(model_size_bytes: float, num_gpus: int) -> float:
    """
    torch.nn.DataParallel re-broadcasts the model from GPU0 to every
    other GPU on EVERY forward pass (it keeps no persistent replicas),
    then gathers every replica's output back to GPU0: roughly
    2 * (num_gpus - 1) * model_size_bytes moved per step.
    """
    # TODO: implement (0.0 for num_gpus <= 1)
    pass


def ddp_communication_volume(model_size_bytes: float, num_gpus: int) -> float:
    """
    torch.nn.parallel.DistributedDataParallel keeps a persistent
    replica on each GPU and only communicates gradients, via one ring
    all-reduce per step -- the standard ring all-reduce volume is
    2 * (num_gpus - 1) / num_gpus * model_size_bytes, independent of
    which GPU is "GPU0".
    """
    # TODO: implement (0.0 for num_gpus <= 1)
    pass


def dp_gpu0_memory_multiplier(num_gpus: int) -> float:
    """
    DataParallel gathers every GPU's forward output (and computes the
    loss/backward start) on GPU0, so GPU0's extra memory load scales
    with num_gpus while every other GPU's doesn't.
    """
    # TODO: return float(num_gpus)
    pass


def ddp_gpu0_memory_multiplier(num_gpus: int) -> float:
    """
    DDP has no such asymmetry -- every rank does the same amount of
    work and holds the same amount of memory, regardless of num_gpus.
    """
    # TODO: return 1.0
    pass


def communication_reduction_factor(model_size_bytes: float, num_gpus: int) -> float:
    """
    How many times more data DataParallel moves per step compared to
    DistributedDataParallel, for the same model size and GPU count.
    """
    # TODO: dp_communication_volume / ddp_communication_volume
    # (return 1.0 when num_gpus <= 1, to avoid dividing by zero)
    pass
