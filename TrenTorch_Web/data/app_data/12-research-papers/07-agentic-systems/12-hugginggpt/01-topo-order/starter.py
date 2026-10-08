def topo_order(tasks):
    """
    tasks: mapping from task id to the list of task ids it depends on

    Returns:
        An execution order in which every task comes after its dependencies, or None if there is a cycle.
    """
    # TODO: Run a topological sort, starting with tasks that have no unmet dependencies (see Theory).
    pass
