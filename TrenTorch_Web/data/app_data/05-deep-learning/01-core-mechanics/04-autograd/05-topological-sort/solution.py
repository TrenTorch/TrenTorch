
from _load import load_solution

Value = load_solution("dl-core-graph-node").Value


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
