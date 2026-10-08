def fsdp_shard_numel(numel, world):
    """
    numel: number of elements in the flattened parameter group
    world: number of data-parallel ranks

    Returns:
        The number of elements each rank stores, numel divided by world, rounded up.
    """
    # TODO: Round numel / world up to a whole number (see Theory).
    pass
