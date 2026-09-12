import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

Value = load_solution("02-deep-learning-core/04-autograd/04-graph-node").Value
build_topo_order = load_solution("02-deep-learning-core/04-autograd/05-topological-sort").build_topo_order


def backward(root: Value) -> None:
    topo_order = build_topo_order(root)
    root.grad = 1.0
    for node in reversed(topo_order):
        node._backward()
