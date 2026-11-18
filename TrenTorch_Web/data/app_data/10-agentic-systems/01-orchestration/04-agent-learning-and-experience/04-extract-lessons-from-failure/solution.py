def extract_lesson(failed_step: str, error_keywords: dict[str, str]) -> str:
    for pattern, lesson in error_keywords.items():
        if pattern in failed_step:
            return lesson
    return "No specific lesson identified -- investigate manually."
