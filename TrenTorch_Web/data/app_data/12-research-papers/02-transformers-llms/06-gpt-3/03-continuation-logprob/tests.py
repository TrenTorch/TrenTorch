"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/06-gpt-3/03-continuation-logprob/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-gpt3-continuation-logprob")
continuation_logprob = _module.continuation_logprob


import numpy as np


def test_1_empty_continuation_has_zero_logprob():
    lp = np.log(np.full((3, 2), 0.5))
    assert continuation_logprob(lp, np.array([0, 1, 0]), 3) == 0.0


def test_2_sums_the_continuation_tokens():
    lp = np.log(np.full((3, 2), 0.5))
    assert abs(continuation_logprob(lp, np.array([0, 1, 0]), 1) - 2 * np.log(0.5)) < 1e-9


def test_3_prompt_tokens_are_not_scored():
    lp = np.log(np.full((2, 2), 0.25))
    assert abs(continuation_logprob(lp, np.array([0, 0]), 1) - np.log(0.25)) < 1e-9


def test_4_more_likely_token_scores_higher():
    lp = np.log(np.array([[0.5, 0.5], [0.9, 0.1]]))
    likely = continuation_logprob(lp, np.array([0, 0]), 1)
    unlikely = continuation_logprob(lp, np.array([0, 1]), 1)
    assert likely > unlikely


def test_5_returns_a_python_float():
    lp = np.log(np.full((2, 2), 0.5))
    assert isinstance(continuation_logprob(lp, np.array([0, 1]), 0), float)


def test_6_does_not_mutate_inputs():
    lp = np.log(np.full((2, 2), 0.5))
    continuation_logprob(lp, np.array([0, 1]), 0)
    np.testing.assert_allclose(lp, np.log(np.full((2, 2), 0.5)))

