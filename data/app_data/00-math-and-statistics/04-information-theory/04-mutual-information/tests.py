"""
pytest data/app_data/00-math-and-statistics/04-information-theory/04-mutual-information/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-math-and-statistics/04-information-theory/{Path(__file__).resolve().parent.name}")
mutual_information = _module.mutual_information


def test_mutual_information_of_independent_variables_is_zero():
    px = np.array([0.5, 0.5])
    py = np.array([0.3, 0.7])
    joint = np.outer(px, py)  # truly independent, by construction
    assert np.isclose(mutual_information(joint), 0.0, atol=1e-9)


def test_mutual_information_is_never_negative():
    rng = np.random.default_rng(0)
    for _ in range(10):
        raw = rng.uniform(size=(3, 3))
        joint = raw / raw.sum()
        assert mutual_information(joint) >= -1e-9


def test_mutual_information_of_strongly_correlated_variables_is_positive():
    # X and Y almost always agree.
    joint = np.array([[0.45, 0.05], [0.05, 0.45]])
    assert mutual_information(joint) > 0.0


def test_mutual_information_of_perfectly_determined_relationship_equals_entropy():
    # When Y is a deterministic function of X (here, Y always equals X),
    # knowing X tells you EVERYTHING about Y, so MI equals the entropy
    # of X (or Y) itself.
    joint = np.array([[0.5, 0.0], [0.0, 0.5]])
    entropy = load_solution("00-math-and-statistics/04-information-theory/01-entropy").entropy
    px = joint.sum(axis=1)
    assert np.isclose(mutual_information(joint), entropy(px), atol=1e-9)


def test_mutual_information_increases_with_stronger_dependence():
    weakly_dependent = np.array([[0.3, 0.2], [0.2, 0.3]])
    strongly_dependent = np.array([[0.45, 0.05], [0.05, 0.45]])
    assert mutual_information(strongly_dependent) > mutual_information(weakly_dependent)


def test_mutual_information_uses_the_outer_product_not_the_joint_itself():
    # Directly targets a mutant that compares the joint against itself
    # instead of against the independent outer product (e.g. computing
    # kl_divergence(joint, joint), which is trivially always 0). Uses a
    # joint with real dependence, where the correct answer must be > 0.
    joint = np.array([[0.4, 0.1], [0.1, 0.4]])
    result = mutual_information(joint)
    assert result > 0.05  # a self-compared mutant would incorrectly give 0.0
