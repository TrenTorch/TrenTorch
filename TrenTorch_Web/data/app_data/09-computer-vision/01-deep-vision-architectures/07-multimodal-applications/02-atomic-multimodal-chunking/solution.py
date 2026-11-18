def chunk_with_atomic_blocks(blocks: list[tuple[str, int]], max_chunk_size: int) -> list[list[str]]:
    chunks: list[list[str]] = []
    current: list[str] = []
    current_size = 0
    for content, size in blocks:
        if current and current_size + size > max_chunk_size:
            chunks.append(current)
            current = []
            current_size = 0
        current.append(content)
        current_size += size
    if current:
        chunks.append(current)
    return chunks
