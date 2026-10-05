def route_modality_for_question(
    question: str, modality_keywords: dict[str, list[str]], default_modality: str
) -> str:
    """`modality_keywords` maps a modality name (e.g. "image", "table") to a
    list of keywords. Return the first modality (in dict insertion order)
    whose keyword list has a case-insensitive substring match in
    `question`. If none match, return `default_modality`.
    """
    # TODO: implement
    pass
