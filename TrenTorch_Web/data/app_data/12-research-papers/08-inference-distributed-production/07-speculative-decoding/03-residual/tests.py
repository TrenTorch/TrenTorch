"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/07-speculative-decoding/03-residual/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-spec-residual")
residual_distribution = _module.residual_distribution


import numpy as np


def test_1_residual_keeps_only_where_target_exceeds_draft():
    np.testing.assert_allclose(residual_distribution(np.array([0.6, 0.4]), np.array([0.3, 0.7])), [1.0, 0.0])


def test_2_mass_where_draft_is_larger_is_discarded():
    np.testing.assert_allclose(residual_distribution(np.array([0.2, 0.8]), np.array([0.5, 0.5])), [0.0, 1.0])


def test_3_result_sums_to_one():
    out = residual_distribution(np.array([0.5, 0.5]), np.array([0.2, 0.2]))
    assert abs(out.sum() - 1.0) < 1e-12


def test_4_hand_value_for_two_tokens():
    np.testing.assert_allclose(residual_distribution(np.array([0.5, 0.5]), np.array([0.2, 0.2])), [0.5, 0.5])


def test_5_result_is_nonnegative():
    out = residual_distribution(np.array([0.1, 0.9]), np.array([0.5, 0.5]))
    assert np.all(out >= 0)


def test_6_does_not_mutate_inputs():
    p = np.array([0.6, 0.4])
    residual_distribution(p, np.array([0.3, 0.7]))
    np.testing.assert_array_equal(p, [0.6, 0.4])

