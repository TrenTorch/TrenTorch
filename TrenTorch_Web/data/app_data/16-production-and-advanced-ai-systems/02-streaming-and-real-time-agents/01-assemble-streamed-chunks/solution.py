def assemble_stream(chunks: list[str]) -> list[str]:
    snapshots = []
    accumulated = ""
    for chunk in chunks:
        accumulated += chunk
        snapshots.append(accumulated)
    return snapshots
