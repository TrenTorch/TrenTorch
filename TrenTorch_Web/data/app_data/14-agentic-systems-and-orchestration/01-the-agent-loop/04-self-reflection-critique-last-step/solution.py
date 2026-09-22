def find_abandon_point(
    observations: list[str], failure_keywords: list[str], max_consecutive_failures: int
) -> int | None:
    consecutive = 0
    for i, observation in enumerate(observations, start=1):
        if any(keyword in observation for keyword in failure_keywords):
            consecutive += 1
        else:
            consecutive = 0
        if consecutive >= max_consecutive_failures:
            return i
    return None
