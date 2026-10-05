"""
pytest tests.py
"""

import math
import pytest
from _load import load_solution

_module = load_solution(__file__)
layer_index = _module.layer_index
layerwise_lr = _module.layerwise_lr


def test_1_layer_indices():
    assert layer_index("embed.weight", 4) == 0
    assert layer_index("layers.0.attn.q", 4) == 1 and layer_index("layers.3.mlp.w", 4) == 4
    assert layer_index("head.bias", 4) == 5


def test_2_head_gets_the_base_rate():
    assert layerwise_lr("head.weight", 4, 1e-3, 0.5) == 1e-3


def test_3_geometric_progression_downwards():
    rates = [layerwise_lr(n, 2, 1.0, 0.5) for n in ("embed.w", "layers.0.w", "layers.1.w", "head.w")]
    assert rates == [0.125, 0.25, 0.5, 1.0]


def test_4_decay_one_is_uniform():
    names = ["embed.w", "layers.2.w", "head.w"]
    assert all(layerwise_lr(n, 3, 0.01, 1.0) == 0.01 for n in names)


def test_5_unknown_names_raise():
    for bad in ("pooler.weight", "layers.x.w", "layers"):
        with pytest.raises(ValueError):
            layer_index(bad, 3)


def test_6_deeper_layers_always_get_larger_rates():
    n = 6
    rates = [layerwise_lr(f"layers.{i}.w", n, 1.0, 0.8) for i in range(n)]
    assert rates == sorted(rates)


def test_7_ratio_between_neighbouring_layers_is_the_decay():
    a, b = layerwise_lr("layers.1.w", 5, 2.0, 0.7), layerwise_lr("layers.2.w", 5, 2.0, 0.7)
    assert math.isclose(a / b, 0.7)
