def score_transcript(transcript: list[tuple[str, str]], rubric: dict[str, int]) -> int:
    total = 0
    for _role, text in transcript:
        for pattern, points in rubric.items():
            if pattern in text:
                total += points
    return total
