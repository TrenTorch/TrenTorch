
from _load import load_solution

Module = load_solution("dl-training-module-base-class").Module


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
