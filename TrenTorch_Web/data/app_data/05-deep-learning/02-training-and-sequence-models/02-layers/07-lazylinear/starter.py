
import numpy as np

from _load import load_solution

Module = load_solution("dl-training-module-base-class").Module
linear_forward = load_solution("dl-training-linear-forward").linear_forward


class LazyLinear(Module):
    """
    A Linear layer that doesn't need `in_features` specified up front: it
    infers it from the shape of the FIRST real input it ever sees, on the
    first call to forward(). Every call after that reuses the SAME weight
    and bias (it does not re-infer or reinitialize on later calls).
    """

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
        pass
