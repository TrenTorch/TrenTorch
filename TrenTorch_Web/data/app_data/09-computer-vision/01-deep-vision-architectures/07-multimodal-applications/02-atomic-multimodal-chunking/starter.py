def chunk_with_atomic_blocks(blocks: list[tuple[str, int]], max_chunk_size: int) -> list[list[str]]:
    """Each block is (content, size) -- content might be a paragraph or an
    image's caption, but either way it's atomic: it must never be split
    across two chunks. Greedily pack blocks into chunks that stay at or
    under `max_chunk_size`, in order. If a single block's own size already
    exceeds `max_chunk_size`, it still becomes its own chunk on its own
    (it can't be split smaller, so it's placed as-is rather than dropped or
    forced to combine with anything else). Return the list of chunks, each
    a list of block contents.
    """
    # TODO: implement
    pass
