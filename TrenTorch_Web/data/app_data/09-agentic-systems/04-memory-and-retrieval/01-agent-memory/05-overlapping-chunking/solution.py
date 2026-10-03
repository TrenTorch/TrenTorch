def chunk_tokens(tokens, size, overlap):
    chunks, start, step = [], 0, size - overlap
    while start < len(tokens):
        chunks.append(list(tokens[start:start + size]))
        if start + size >= len(tokens):
            break
        start += step
    return chunks
