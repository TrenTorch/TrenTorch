def fsdp_padded_numel(numel, world):
    """
    numel: number of parameters in the group
    world: number of ranks

    Returns:
        The flat buffer size after padding so it divides evenly into world shards.
    """
    # TODO: Round numel up to the next multiple of world (see Theory).
    pass
