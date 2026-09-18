import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

Value = load_solution("02-deep-learning-core/04-autograd/04-graph-node").Value


def build_topo_order(root: Value) -> list[Value]:
    visited = set()
    topo_order = []

    def visit(node: Value):
        if node not in visited:
            visited.add(node)
            for parent in node._prev:
                visit(parent)
            topo_order.append(node)

    visit(root)
    return topo_order
