def fsdp_padded_numel(numel, world):
    return -(-numel // world) * world
