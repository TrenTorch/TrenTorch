
from _load import load_solution

Value = load_solution("dl-core-graph-node").Value
build_topo_order = load_solution("dl-core-topological-sort").build_topo_order


def backward(root: Value) -> None:
    """
    The final assembly: a full, general `.backward()` for ANY
    expression built from Value's __add__/__mul__, however deep or
    however many times a node gets reused.

    1. Build the topological order from `root` (Topological sort for
       backward pass, already provided above).
    2. Seed `root.grad = 1.0` (the derivative of anything with respect
       to itself is 1, the starting point every backward pass needs).
    3. Walk the topo order in REVERSE (root first, leaves last), calling
       each node's `_backward()` in that order, exactly the order
       Topological sort for backward pass's own Theory section explains.

    After this runs, every Value reachable from `root` has its correct
    `.grad` populated, no further calls needed.
    """
    pass
