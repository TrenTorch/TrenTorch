"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
import pytest

pool_sentence = _module.pool_sentence
H = np.array([[[1.0, 4.0], [3.0, 2.0], [100.0, 100.0]], [[5.0, 5.0], [7.0, 1.0], [9.0, 9.0]]])
M = np.array([[1, 1, 0], [1, 1, 1]])


def test_1_cls():
    assert np.allclose(pool_sentence(H, M, "cls"), [[1.0, 4.0], [5.0, 5.0]])


def test_2_mean_ignores_padding():
    assert np.allclose(pool_sentence(H, M, "mean"), [[2.0, 3.0], [7.0, 5.0]])


def test_3_max_ignores_padding():
    assert np.allclose(pool_sentence(H, M, "max"), [[3.0, 4.0], [9.0, 9.0]])


def test_4_padding_contents_do_not_matter():
    H2 = H.copy()
    H2[0, 2] = -999.0
    for mode in ("cls", "mean", "max"):
        assert np.allclose(pool_sentence(H, M, mode), pool_sentence(H2, M, mode))


def test_5_unknown_mode_raises():
    with pytest.raises(ValueError):
        pool_sentence(H, M, "last")


def test_6_all_real_tokens_equals_plain_mean_and_max():
    h = np.random.RandomState(0).randn(3, 5, 4)
    m = np.ones((3, 5), dtype=int)
    assert np.allclose(pool_sentence(h, m, "mean"), h.mean(axis=1)) and np.allclose(pool_sentence(h, m, "max"), h.max(axis=1))


def test_7_inputs_untouched_and_output_shape():
    h, m = H.copy(), M.copy()
    out = pool_sentence(h, m, "mean")
    assert out.shape == (2, 2) and np.array_equal(h, H) and np.array_equal(m, M)
