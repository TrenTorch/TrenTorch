"""
pytest data/app_data/03-dl-training/02-layers/06-sequential-container/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"03-dl-training/02-layers/{Path(__file__).resolve().parent.name}")
Sequential = _module.Sequential
Module = load_solution("03-dl-training/02-layers/05-module-base-class").Module


class AddConstant(Module):
    def __init__(self, value):
        super().__init__()
        self.value = value
        self.register_parameter("value", np.array([value]))

    def forward(self, x):
        return x + self.value


class MultiplyConstant(Module):
    def __init__(self, value):
        super().__init__()
        self.value = value
        self.register_parameter("value", np.array([value]))

    def forward(self, x):
        return x * self.value


def test_chains_two_layers_in_order():
    model = Sequential(AddConstant(3), MultiplyConstant(2))
    # (5 + 3) * 2 = 16
    assert model.forward(5) == 16


def test_order_matters_reversed_layers_give_a_different_result():
    model = Sequential(MultiplyConstant(2), AddConstant(3))
    # (5 * 2) + 3 = 13
    assert model.forward(5) == 13


def test_single_layer_sequential_applies_just_that_layer():
    model = Sequential(AddConstant(10))
    assert model.forward(5) == 15


def test_empty_sequential_returns_input_unchanged():
    model = Sequential()
    assert model.forward(42) == 42


def test_three_layers_chain_correctly():
    model = Sequential(AddConstant(1), AddConstant(2), MultiplyConstant(10))
    # ((5 + 1) + 2) * 10 = 80
    assert model.forward(5) == 80


def test_parameters_collects_every_layers_parameters():
    model = Sequential(AddConstant(3), MultiplyConstant(2), AddConstant(7))
    params = model.parameters()
    assert len(params) == 3
    values = sorted(p.item() for p in params)
    assert values == [2.0, 3.0, 7.0]


def test_forward_feeds_each_layers_output_as_the_next_layers_input_not_the_original_x():
    # Directly targets a mutant that re-applies every layer to the
    # ORIGINAL x instead of chaining outputs (e.g. `for layer in
    # self.layers: result = layer.forward(x)`, forgetting to reassign x),
    # which would make only the LAST layer's effect visible.
    model = Sequential(AddConstant(100), MultiplyConstant(2))
    # correct chained result: (5 + 100) * 2 = 210
    # broken (each layer sees original x=5): last layer wins -> 5*2=10
    assert model.forward(5) == 210
