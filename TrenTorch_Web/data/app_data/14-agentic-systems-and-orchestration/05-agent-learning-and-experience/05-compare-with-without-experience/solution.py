def compare_experience_impact(
    with_experience: list[bool], without_experience: list[bool]
) -> dict:
    n = len(with_experience)
    with_rate = sum(with_experience) / n
    without_rate = sum(without_experience) / n
    tasks_only_with_helped = sum(
        1 for w, wo in zip(with_experience, without_experience) if w and not wo
    )
    return {
        "with_success_rate": with_rate,
        "without_success_rate": without_rate,
        "tasks_only_with_helped": tasks_only_with_helped,
        "delta": with_rate - without_rate,
    }
