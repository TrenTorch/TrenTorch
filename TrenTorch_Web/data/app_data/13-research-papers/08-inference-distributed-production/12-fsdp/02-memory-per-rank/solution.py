def fsdp_memory_per_rank(numel, world, nbytes):
    return -(-numel // world) * nbytes
