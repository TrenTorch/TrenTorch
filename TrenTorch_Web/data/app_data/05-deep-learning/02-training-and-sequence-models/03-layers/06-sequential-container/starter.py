
from _load import load_solution

Module = load_solution("dl-training-module-base-class").Module


class Sequential(Module):
    """
    Chains a list of layers together: calling forward(x) on a Sequential
    runs x through the FIRST layer, feeds that layer's output into the
    SECOND layer, and so on, returning the last layer's output.

    Also registers every layer as a child module (via `[05-module-base-
    class]`'s `register_module`), so calling `.parameters()` on a
    Sequential automatically collects every layer's parameters too.
    """

    def __init__(self, *layers):
        super().__init__()
        pass

    def forward(self, x):
        pass
