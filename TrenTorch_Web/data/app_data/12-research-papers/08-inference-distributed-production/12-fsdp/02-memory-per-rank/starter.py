def fsdp_memory_per_rank(numel, world, nbytes):
    """
    numel: number of parameters in the group
    world: number of ranks
    nbytes: bytes per parameter

    Returns:
        The bytes of the parameter shard stored on each rank.
    """
    # TODO: Multiply the rounded-up shard size by the bytes per element (see Theory).
    pass
