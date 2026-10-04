def truncate_at_stop(text: str, stops: list[str]):
    """Return (clean_text, hit): cut at the earliest occurrence of any stop string."""
    # TODO
    pass


def safe_emit_length(buffer: str, stops: list[str]) -> int:
    """Characters that can be emitted now without risking sending part of a stop sequence."""
    # TODO
    pass
