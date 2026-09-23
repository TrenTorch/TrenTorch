def extract_lesson(failed_step: str, error_keywords: dict[str, str]) -> str:
    """
    failed_step: the text describing what the failed step actually did
    or reported.
    error_keywords: an ordered mapping from a substring pattern to the
    lesson text for that category of failure.

    Return the lesson for the FIRST pattern (in error_keywords'
    iteration/insertion order) that appears as a substring anywhere in
    failed_step. If no pattern matches, return the literal string
    "No specific lesson identified -- investigate manually."
    """
    # TODO: Implement the first-match lesson lookup from Theory.
    pass
