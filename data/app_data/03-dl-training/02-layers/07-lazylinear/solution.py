import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

Module = load_solution("03-dl-training/02-layers/05-module-base-class").Module
linear_forward = load_solution("03-dl-training/02-layers/01-linear-forward").linear_forward


class LazyLinear(Module):
    def __init__(self, out_features, weight_init=None, bias_init=None):
        super().__init__()
        self.out_features = out_features
        self.weight_init = weight_init or (
            lambda in_features, out_features: np.zeros((out_features, in_features))
        )
        self.bias_init = bias_init or (lambda out_features: np.zeros(out_features))
        self.weight = None
        self.bias = None

    def forward(self, x):
        if self.weight is None:
            in_features = x.shape[-1]
            self.weight = self.weight_init(in_features, self.out_features)
            self.bias = self.bias_init(self.out_features)
            self.register_parameter("weight", self.weight)
            self.register_parameter("bias", self.bias)
        return linear_forward(x, self.weight, self.bias)
