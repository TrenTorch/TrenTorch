"""
pytest data/app_data/01-classical-ml/05-instance-based-probabilistic/06-spectral-drift-gp-calibration/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"01-classical-ml/05-instance-based-probabilistic/{Path(__file__).resolve().parent.name}"
)
rydberg_wavelength_nm = _module.rydberg_wavelength_nm
gp_calibrate = _module.gp_calibrate


def test_example_one_matches_the_specs_worked_derivation():
    training = [(2, 3, 656.3), (2, 4, 486.15), (2, 5, 434.10)]
    result = gp_calibrate(training, sigma_f=0.2, l=50.0, sigma_n=0.05, queries=[(2, 6), (1, 2)])
    expected = np.array([[410.195499, 0.091764], [121.502291, 0.200000]])
    assert np.allclose(result, expected, atol=1e-4)


def test_example_two_matches_the_specs_worked_derivation():
    training = [(2, 3, 656.28), (2, 4, 486.12), (2, 5, 434.08), (2, 6, 410.05)]
    result = gp_calibrate(training, sigma_f=0.15, l=20.0, sigma_n=0.02, queries=[(2, 7), (3, 4)])
    expected = np.array([[396.851586, 0.083163], [1874.606772, 0.150000]])
    assert np.allclose(result, expected, atol=1e-4)


def test_rydberg_formula_matches_known_balmer_alpha_wavelength():
    # H-alpha, n2=3 -> n1=2, the ~656 nm Balmer line, computed with this
    # problem's mandated R_H (not the more commonly quoted CODATA value,
    # which lands closer to 656.28 nm -- see the precision test below).
    assert abs(rydberg_wavelength_nm(2, 3) - 656.112370) < 1e-4


def test_rydberg_formula_uses_the_mandated_constant_precisely():
    # A commonly-quoted-but-different R_H (e.g. 1.0967758e7, the CODATA
    # value rather than this problem's mandated 1.097373e7) shifts the
    # theoretical wavelength by more than the 1e-4 tolerance -- this test
    # fails for anyone who hardcoded a different textbook constant.
    wrong_r_h_wavelength = 1.0 / (1.0967758e7 * (1.0 / 2**2 - 1.0 / 3**2)) * 1e9
    assert abs(rydberg_wavelength_nm(2, 3) - wrong_r_h_wavelength) > 1e-3


def test_pure_extrapolation_across_series_reverts_exactly_to_the_prior():
    # Only Balmer training data; a Paschen query is over a thousand nm
    # away -- the RBF correlation is ~0, so the posterior must revert
    # exactly to (0 correction, sigma_f uncertainty).
    training = [(2, 3, 656.25), (2, 4, 486.10), (2, 5, 434.05)]
    sigma_f = 0.3
    result = gp_calibrate(training, sigma_f=sigma_f, l=10.0, sigma_n=0.05, queries=[(3, 4)])
    x_star = rydberg_wavelength_nm(3, 4)
    assert abs(result[0, 0] - x_star) < 1e-4  # zero correction
    assert abs(result[0, 1] - sigma_f) < 1e-4  # uncertainty == sigma_f exactly


def test_very_small_sigma_n_reproduces_a_training_residual_almost_exactly():
    # Near-noiseless training data: querying at (a transition matching) a
    # training input should recover that point's exact residual, with
    # uncertainty collapsing close to zero.
    training = [(2, 3, 656.30), (2, 4, 486.20), (2, 5, 434.00)]
    result = gp_calibrate(training, sigma_f=0.5, l=100.0, sigma_n=1e-6, queries=[(2, 4)])
    x_star = rydberg_wavelength_nm(2, 4)
    expected_measured = 486.20
    assert abs(result[0, 0] - expected_measured) < 1e-3
    assert result[0, 1] < 1e-3


def test_very_small_length_scale_reverts_every_query_to_the_prior():
    # l far shorter than the spacing between training points: even a
    # query "between" two training points sees ~0 correlation with both.
    training = [(2, 3, 656.40), (2, 4, 486.25)]
    sigma_f = 0.25
    result = gp_calibrate(training, sigma_f=sigma_f, l=1e-6, sigma_n=0.05, queries=[(2, 5)])
    x_star = rydberg_wavelength_nm(2, 5)
    assert abs(result[0, 0] - x_star) < 1e-4
    assert abs(result[0, 1] - sigma_f) < 1e-3


def test_very_large_length_scale_learns_one_global_offset():
    # l >> the spread of training x's: the kernel is ~constant across all
    # of them, so the GP should predict close to the same offset (the
    # mean residual) for every query, near-independent of x_star.
    training = [(2, 3, 656.35), (2, 4, 486.20), (2, 5, 434.15), (2, 6, 410.10)]
    result = gp_calibrate(training, sigma_f=0.5, l=1e4, sigma_n=0.02, queries=[(2, 7), (2, 8)])
    corrections = result[:, 0] - np.array(
        [rydberg_wavelength_nm(2, 7), rydberg_wavelength_nm(2, 8)]
    )
    assert abs(corrections[0] - corrections[1]) < 1e-3


def test_single_training_point_degenerates_correctly():
    # n=1: the 1x1 Cholesky/posterior formulas must not special-case-crash.
    training = [(2, 3, 656.35)]
    result = gp_calibrate(training, sigma_f=0.2, l=50.0, sigma_n=0.05, queries=[(2, 3)])
    assert result.shape == (1, 2)
    assert np.all(np.isfinite(result))


def test_dense_interpolation_stays_accurate_with_closely_spaced_points():
    # Many training x's close together -- checks the Cholesky solve
    # doesn't degrade with an ill-conditioned (but still PD) K.
    rng = np.random.default_rng(0)
    training = [(2, 3 + i, 656.3 - 0.01 * i) for i in range(1, 21)]
    result = gp_calibrate(training, sigma_f=0.3, l=5.0, sigma_n=0.03, queries=[(2, 15)])
    assert np.all(np.isfinite(result))
    assert result[0, 1] >= 0.0


def test_high_n_transitions_stay_precise_near_the_series_limit():
    # n1, n2 up to 30: theoretical wavelengths bunch up tightly as n2
    # grows for fixed n1, stressing the Rydberg formula's own precision
    # independent of the GP machinery.
    w29 = rydberg_wavelength_nm(2, 29)
    w30 = rydberg_wavelength_nm(2, 30)
    assert w29 != w30
    assert 0 < (w29 - w30) < 1.0


def test_predict_shape_matches_number_of_queries():
    training = [(2, 3, 656.3), (2, 4, 486.15)]
    result = gp_calibrate(training, sigma_f=0.2, l=50.0, sigma_n=0.05, queries=[(2, 5), (2, 6), (1, 2)])
    assert result.shape == (3, 2)
