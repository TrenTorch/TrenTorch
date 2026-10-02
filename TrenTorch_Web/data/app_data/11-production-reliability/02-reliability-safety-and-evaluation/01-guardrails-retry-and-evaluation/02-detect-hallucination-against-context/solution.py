def detect_hallucination(claim_sentences: list[str], context_sentences: list[str]) -> list[bool]:
    return [
        not any(claim in context for context in context_sentences)
        for claim in claim_sentences
    ]
