"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/04-distillation/01-softmax-temperature/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-distill-softmax-temperature")
softmax_temperature = _module.softmax_temperature


import numpy as np


def test_1_temperature_one_is_the_ordinary_softmax():
    z = np.array([1.0, 2.0, 3.0])
    expected = np.exp(z) / np.exp(z).sum()
    np.testing.assert_allclose(softmax_temperature(z, 1.0), expected)


def test_2_high_temperature_flattens_the_distribution():
    out = softmax_temperature(np.array([0.0, 10.0]), 1000.0)
    np.testing.assert_allclose(out, [0.5, 0.5], atol=0.01)


def test_3_rows_sum_to_one():
    out = softmax_temperature(np.array([[1.0, 2.0], [5.0, -5.0]]), 2.0)
    np.testing.assert_allclose(out.sum(axis=-1), 1.0)


def test_4_equal_logits_give_uniform_output():
    np.testing.assert_allclose(softmax_temperature(np.zeros(4), 3.0), [0.25] * 4)


def test_5_ordering_of_classes_is_preserved():
    out = softmax_temperature(np.array([1.0, 3.0, 2.0]), 2.0)
    assert out[1] > out[2] > out[0]


def test_6_does_not_mutate_the_logits():
    z = np.array([1.0, 2.0])
    softmax_temperature(z, 2.0)
    np.testing.assert_array_equal(z, [1.0, 2.0])

