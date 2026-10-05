
from _load import load_solution

Value = load_solution("dl-core-graph-node").Value
build_topo_order = load_solution("dl-core-topological-sort").build_topo_order


def backward(root: Value) -> None:
    topo_order = build_topo_order(root)
    root.grad = 1.0
    for node in reversed(topo_order):
        node._backward()
