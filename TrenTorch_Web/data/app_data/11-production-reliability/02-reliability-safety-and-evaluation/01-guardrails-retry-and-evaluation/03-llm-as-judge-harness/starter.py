def score_transcript(transcript: list[tuple[str, str]], rubric: dict[str, int]) -> int:
    """
    transcript: (role, text) turns making up one agent run, in order.
    rubric: a substring pattern -> point value (may be negative),
    representing a deterministic stand-in for an LLM judge's scoring
    criteria.

    For each turn's text, add every rubric pattern's point value to a
    running total if that pattern appears anywhere in that turn's text
    (each pattern counts at most once PER TURN, even if it appears
    multiple times within that turn's text).

    Returns the total score across the whole transcript.
    """
    # TODO: Implement the deterministic rubric scorer from Theory.
    pass
