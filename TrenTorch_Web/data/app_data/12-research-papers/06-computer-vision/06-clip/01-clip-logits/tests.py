"""
pytest data/app_data/12-research-papers/06-computer-vision/06-clip/01-clip-logits/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-clip-logits")
clip_logits = _module.clip_logits


import numpy as np


def test_1_output_is_square_over_the_batch():
    assert clip_logits(np.ones((3, 4)), np.ones((3, 4)), 0.07).shape == (3, 3)


def test_2_identical_pairs_have_similarity_one_over_temperature():
    e = np.array([[1.0, 0.0], [0.0, 1.0]])
    logits = clip_logits(e, e, 1.0)
    np.testing.assert_allclose(np.diag(logits), [1.0, 1.0])


def test_3_scale_of_embeddings_does_not_matter():
    a = np.array([[1.0, 2.0]])
    b = np.array([[3.0, 1.0]])
    np.testing.assert_allclose(clip_logits(a, b, 1.0), clip_logits(10 * a, 5 * b, 1.0))


def test_4_temperature_scales_the_logits():
    a = np.array([[1.0, 0.0]])
    np.testing.assert_allclose(clip_logits(a, a, 0.5), [[2.0]])


def test_5_orthogonal_pairs_have_zero_logit():
    logits = clip_logits(np.array([[1.0, 0.0]]), np.array([[0.0, 1.0]]), 1.0)
    np.testing.assert_allclose(logits, [[0.0]], atol=1e-12)


def test_6_does_not_mutate_inputs():
    a = np.array([[2.0, 0.0]])
    clip_logits(a, a, 1.0)
    np.testing.assert_array_equal(a, [[2.0, 0.0]])

