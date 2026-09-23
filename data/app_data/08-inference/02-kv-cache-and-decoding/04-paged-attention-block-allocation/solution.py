def paged_attention_allocate(block_size: int, total_blocks: int, events: list) -> dict:
    free_blocks = list(range(total_blocks))
    seq_tables: dict = {}
    seq_len: dict = {}
    oom_at = None

    for i, (op, seq_id) in enumerate(events):
        if op == "append":
            table = seq_tables.setdefault(seq_id, [])
            n = seq_len.get(seq_id, 0)
            needs_new_block = n % block_size == 0
            if needs_new_block:
                if not free_blocks:
                    oom_at = i
                    break
                table.append(free_blocks.pop(0))
            seq_len[seq_id] = n + 1
        elif op == "free":
            if seq_id in seq_tables:
                free_blocks.extend(seq_tables.pop(seq_id))
                free_blocks.sort()
                seq_len.pop(seq_id, None)
        else:
            raise ValueError(f"unknown op {op!r}")

    return {
        "block_tables": {str(k): v for k, v in seq_tables.items()},
        "free_blocks_remaining": len(free_blocks),
        "out_of_memory_at_event": oom_at,
    }
