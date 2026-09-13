"""
pytest data/app_data/07-vision/05-cnn-architecture-history/04-efficientnet-compound-scaling/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

compound_scale = load_solution(
    f"07-vision/05-cnn-architecture-history/{Path(__file__).resolve().parent.name}"
).compound_scale


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_phi_zero_gives_no_scaling_at_all():
    depth, width, resolution = compound_scale(phi=0)
    assert depth == 1.0
    assert width == 1.0
    assert resolution == 1.0


def test_02_phi_one_matches_the_base_multipliers_directly():
    depth, width, resolution = compound_scale(phi=1, alpha=1.2, beta=1.1, gamma=1.15)
    assert abs(depth - 1.2) < 1e-9
    assert abs(width - 1.1) < 1e-9
    assert abs(resolution - 1.15) < 1e-9


# --- Shape / general-case coverage -----------------------------------


def test_03_all_three_multipliers_grow_with_phi():
    d1, w1, r1 = compound_scale(phi=1)
    d2, w2, r2 = compound_scale(phi=2)
    d3, w3, r3 = compound_scale(phi=3)
    assert d1 < d2 < d3
    assert w1 < w2 < w3
    assert r1 < r2 < r3


def test_04_matches_direct_exponentiation_for_arbitrary_phi():
    alpha, beta, gamma = 1.2, 1.1, 1.15
    for phi in [1, 2, 4, 5]:
        depth, width, resolution = compound_scale(phi, alpha=alpha, beta=beta, gamma=gamma)
        assert abs(depth - alpha**phi) < 1e-9
        assert abs(width - beta**phi) < 1e-9
        assert abs(resolution - gamma**phi) < 1e-9


# --- Parameter handling -------------------------------------------------


def test_05_custom_base_multipliers_are_respected():
    depth, width, resolution = compound_scale(phi=2, alpha=1.5, beta=1.0, gamma=2.0)
    assert abs(depth - 2.25) < 1e-9  # 1.5^2
    assert abs(width - 1.0) < 1e-9  # 1.0^2
    assert abs(resolution - 4.0) < 1e-9  # 2.0^2


# --- Edge cases ---------------------------------------------------------


def test_06_alpha_beta_gamma_of_exactly_one_never_scales_regardless_of_phi():
    for phi in [0, 1, 3, 10]:
        depth, width, resolution = compound_scale(phi, alpha=1.0, beta=1.0, gamma=1.0)
        assert depth == 1.0
        assert width == 1.0
        assert resolution == 1.0


# --- Return shape / conventions -----------------------------------------


def test_07_returns_a_three_element_tuple_of_floats():
    result = compound_scale(phi=2)
    assert isinstance(result, tuple)
    assert len(result) == 3
    assert all(isinstance(v, float) for v in result)


# --- Independent correctness oracle -----------------------------------


def test_08_recommended_base_multipliers_approximately_satisfy_the_papers_resource_constraint():
    # This is a pure-math relationship stated directly in the EfficientNet
    # paper (Tan & Le, 2019), not something that needs a deep learning
    # library to verify: doubling depth roughly doubles compute (FLOPs
    # scale linearly with depth), but doubling width or resolution
    # roughly QUADRUPLES compute (FLOPs scale quadratically with either,
    # since both spatial dimensions or both weight-matrix dimensions
    # scale together). The paper picks alpha, beta, gamma so that
    # increasing phi by 1 multiplies total compute by roughly a constant
    # factor of 2, under the constraint alpha * beta^2 * gamma^2 ~= 2.
    alpha, beta, gamma = 1.2, 1.1, 1.15
    depth, width, resolution = compound_scale(phi=1, alpha=alpha, beta=beta, gamma=gamma)
    approx_total_compute_multiplier = depth * (width**2) * (resolution**2)
    assert abs(approx_total_compute_multiplier - 2.0) < 0.1
