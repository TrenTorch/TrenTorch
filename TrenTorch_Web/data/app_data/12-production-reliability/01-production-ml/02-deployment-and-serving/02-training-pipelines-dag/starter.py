from collections import deque


def create_dag() -> dict:
    """
    An empty pipeline: a mapping from task name to the list of tasks
    it depends on (tasks that must run BEFORE it).
    """
    # TODO: return {}
    pass


def add_task(dag: dict, task_name: str, depends_on: list | None = None) -> dict:
    """
    Registers a task and its explicit dependencies -- a "notebook run
    top to bottom" has no such record at all, which is exactly the gap
    a real pipeline DAG closes: every dependency has to be written
    down, not just implied by cell order.
    """
    # TODO: dag[task_name] = list(depends_on) if depends_on else [].
    # Return dag.
    pass


def topological_order(dag: dict) -> list:
    """
    Computes a valid execution order (Kahn's algorithm): a task never
    appears before any task it depends on. Raises ValueError if the
    DAG contains a cycle (some tasks would need to run before
    themselves, which is impossible).

    For determinism, break ties among tasks that become "ready" at
    the same time by sorting them alphabetically.
    """
    # TODO: compute each task's in-degree (len of its depends_on list).
    # Build a reverse adjacency map: dependency -> list of tasks that
    # depend on it. Seed a queue with all zero-in-degree tasks
    # (sorted). Repeatedly pop a task, append it to `order`, and for
    # each of ITS dependents (sorted), decrement their in-degree,
    # enqueueing any that hit zero. If `order` ends up shorter than
    # `dag`, raise ValueError (a cycle prevented some tasks from ever
    # reaching zero in-degree).
    pass


def has_cycle(dag: dict) -> bool:
    """
    Whether the DAG actually contains a cycle -- built directly on top
    of topological_order rather than reimplementing cycle detection
    from scratch.
    """
    # TODO: try topological_order(dag); return False if it succeeds,
    # True if it raises ValueError.
    pass
