from collections import deque


def create_dag() -> dict:
    return {}


def add_task(dag: dict, task_name: str, depends_on: list | None = None) -> dict:
    dag[task_name] = list(depends_on) if depends_on else []
    return dag


def topological_order(dag: dict) -> list:
    in_degree = {task: len(deps) for task, deps in dag.items()}
    dependents = {task: [] for task in dag}
    for task, deps in dag.items():
        for dep in deps:
            dependents[dep].append(task)

    queue = deque(sorted(task for task, degree in in_degree.items() if degree == 0))
    order = []
    while queue:
        task = queue.popleft()
        order.append(task)
        for dependent in sorted(dependents[task]):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)

    if len(order) != len(dag):
        raise ValueError("cycle detected: DAG cannot be topologically ordered")
    return order


def has_cycle(dag: dict) -> bool:
    try:
        topological_order(dag)
        return False
    except ValueError:
        return True
