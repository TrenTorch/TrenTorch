def paged_attention_allocate(block_size: int, total_blocks: int, events: list) -> dict:
    """
    events: list of ("append", seq_id) or ("free", seq_id) tuples, in order.

    Returns a dict with keys "block_tables" (seq_id -> list of physical
    block ids), "free_blocks_remaining", and "out_of_memory_at_event"
    (the event index that failed, or None if none did).
    """
    # TODO: Walk events in order. On "append", allocate a new block only
    # when the sequence's token count is an exact multiple of
    # block_size (see Theory). On "free", return all of that sequence's
    # blocks to the free list.
    pass
