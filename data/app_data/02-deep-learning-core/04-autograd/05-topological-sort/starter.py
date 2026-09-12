import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

Value = load_solution("02-deep-learning-core/04-autograd/04-graph-node").Value


def build_topo_order(root: Value) -> list[Value]:
    """
    Returns every Value node reachable from `root` (via `_prev`),
    ordered so that every node appears AFTER all of its own parents
    (the nodes it was built from). `root` itself is last, since
    everything else in the graph is, directly or indirectly, one of
    its ancestors.

    This is a standard post-order depth-first traversal: recurse into
    a node's parents FIRST, then append the node itself, after both
    recursive calls return. Track visited nodes to avoid processing
    the same node twice (a node used in multiple places, like
    Graph node's own accumulation example, would otherwise appear
    more than once).

    See Theory for why THIS specific order is exactly what a correct
    backward pass needs, once reversed.
    """
    pass
