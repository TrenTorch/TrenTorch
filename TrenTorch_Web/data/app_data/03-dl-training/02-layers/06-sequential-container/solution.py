import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

Module = load_solution("03-dl-training/02-layers/05-module-base-class").Module


class Sequential(Module):
    def __init__(self, *layers):
        super().__init__()
        self.layers = list(layers)
        for i, layer in enumerate(self.layers):
            self.register_module(str(i), layer)

    def forward(self, x):
        for layer in self.layers:
            x = layer.forward(x)
        return x
