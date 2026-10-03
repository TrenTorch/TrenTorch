def filter_quality(examples: list[str], min_length: int, banned_phrases: list[str]) -> list[str]:
    lowered_banned = [phrase.lower() for phrase in banned_phrases]
    kept = []
    for example in examples:
        if len(example) < min_length:
            continue
        lowered_example = example.lower()
        if any(phrase in lowered_example for phrase in lowered_banned):
            continue
        kept.append(example)
    return kept
