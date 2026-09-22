def route_modality_for_question(
    question: str, modality_keywords: dict[str, list[str]], default_modality: str
) -> str:
    lowered = question.lower()
    for modality, keywords in modality_keywords.items():
        if any(keyword.lower() in lowered for keyword in keywords):
            return modality
    return default_modality
