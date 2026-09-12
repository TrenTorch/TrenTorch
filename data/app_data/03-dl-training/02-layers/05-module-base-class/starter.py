import numpy as np


class Module:
    """
    A minimal version of torch.nn.Module: something layers can inherit
    from so a whole network's worth of learnable parameters, scattered
    across many nested layers, can be collected into a single flat list
    with one call, exactly what an optimizer needs to iterate over.
    """

    def __init__(self):
        self._parameters: dict[str, np.ndarray] = {}
        self._modules: dict[str, "Module"] = {}

    def register_parameter(self, name: str, value: np.ndarray) -> None:
        """Stores `value` under `name` in this module's own parameter dict."""
        pass

    def register_module(self, name: str, module: "Module") -> None:
        """Stores a CHILD Module under `name`, so its parameters are picked
        up too when parameters() is called on this (parent) module."""
        pass

    def parameters(self) -> list[np.ndarray]:
        """
        Returns a flat list of every parameter registered directly on this
        module, PLUS every parameter registered on every child module
        (and their children, recursively, to any depth).
        """
        pass
