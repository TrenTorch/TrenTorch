def replay_until_failure(steps: list[tuple[str, bool]]) -> list[str]:
    replayed = []
    for name, succeeded in steps:
        replayed.append(name)
        if not succeeded:
            break
    return replayed
