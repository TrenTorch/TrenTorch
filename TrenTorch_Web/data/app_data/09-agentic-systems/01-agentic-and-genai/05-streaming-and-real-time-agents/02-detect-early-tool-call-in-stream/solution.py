def detect_early_tool_call(chunks: list[str], marker: str) -> int | None:
    accumulated = ""
    for i, chunk in enumerate(chunks):
        accumulated += chunk
        if marker in accumulated:
            return i
    return None
