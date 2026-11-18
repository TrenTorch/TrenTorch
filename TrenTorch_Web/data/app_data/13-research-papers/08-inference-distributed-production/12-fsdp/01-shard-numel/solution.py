def fsdp_shard_numel(numel, world):
    return -(-numel // world)
