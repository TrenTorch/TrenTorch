def order_subtasks(subtasks: list[str], dependencies: list[tuple[str, str]]) -> list[str]:
    dependents: dict[str, list[str]] = {s: [] for s in subtasks}
    indegree: dict[str, int] = {s: 0 for s in subtasks}
    for before, after in dependencies:
        dependents[before].append(after)
        indegree[after] += 1

    placed: list[str] = []
    remaining = set(subtasks)

    while remaining:
        next_task = next(s for s in subtasks if s in remaining and indegree[s] == 0)
        placed.append(next_task)
        remaining.remove(next_task)
        for dependent in dependents[next_task]:
            indegree[dependent] -= 1

    return placed
