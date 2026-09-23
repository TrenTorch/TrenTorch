import numpy as np


class Module:
    def __init__(self):
        self._parameters: dict[str, np.ndarray] = {}
        self._modules: dict[str, "Module"] = {}

    def register_parameter(self, name: str, value: np.ndarray) -> None:
        self._parameters[name] = value

    def register_module(self, name: str, module: "Module") -> None:
        self._modules[name] = module

    def parameters(self) -> list[np.ndarray]:
        params = list(self._parameters.values())
        for submodule in self._modules.values():
            params.extend(submodule.parameters())
        return params
