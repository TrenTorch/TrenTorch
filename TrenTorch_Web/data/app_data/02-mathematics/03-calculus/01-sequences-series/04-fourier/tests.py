"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
fourier_coefficients = _module.fourier_coefficients
fourier_series_eval = _module.fourier_series_eval
dft = _module.dft
inverse_dft = _module.inverse_dft
dominant_frequency = _module.dominant_frequency


def _signal(n=64, seed=0):
    rng = np.random.default_rng(seed)
    return rng.normal(size=n)


# ---- 1-5: Fourier series ----


def test_1_recovers_the_weights_of_a_known_trigonometric_polynomial():
    period = 2.0
    f = lambda t: 3.0 + 2.0 * np.cos(2 * np.pi * t / period) - 0.5 * np.sin(2 * np.pi * 3 * t / period)
    a0, a, b = fourier_coefficients(f, period, 4)
    assert np.isclose(a0, 6.0)  # a0 / 2 is the average, 3
    np.testing.assert_allclose(a, [2.0, 0.0, 0.0, 0.0], atol=1e-10)
    np.testing.assert_allclose(b, [0.0, 0.0, -0.5, 0.0], atol=1e-10)


def test_2_square_wave_has_the_known_odd_harmonic_weights():
    period = 1.0
    square = lambda t: np.where((t % period) < period / 2, 1.0, -1.0)
    a0, a, b = fourier_coefficients(square, period, 6, num_samples=100_000)
    expected_b = [4 / (np.pi * k) if k % 2 == 1 else 0.0 for k in range(1, 7)]
    np.testing.assert_allclose(b, expected_b, atol=1e-3)
    np.testing.assert_allclose(a, np.zeros(6), atol=1e-3)
    assert abs(a0) < 1e-3


def test_3_series_reproduces_a_trigonometric_polynomial_exactly():
    period = 5.0
    f = lambda t: 1.0 + np.cos(2 * np.pi * t / period) + 0.25 * np.sin(2 * np.pi * 2 * t / period)
    a0, a, b = fourier_coefficients(f, period, 3)
    t = np.linspace(-7, 7, 29)
    np.testing.assert_allclose(fourier_series_eval(a0, a, b, period, t), f(t), atol=1e-10)


def test_4_series_eval_works_on_a_scalar_and_matches_the_array_form():
    a0, a, b = 2.0, np.array([1.0, 0.5]), np.array([0.0, -1.0])
    scalar = fourier_series_eval(a0, a, b, 4.0, 0.7)
    array = fourier_series_eval(a0, a, b, 4.0, np.array([0.7]))
    assert np.isscalar(scalar) or np.ndim(scalar) == 0
    assert np.isclose(scalar, array[0])


def test_5_zero_terms_gives_the_average_only():
    a0, a, b = fourier_coefficients(lambda t: np.full_like(t, 5.0), 3.0, 0)
    assert np.isclose(a0, 10.0) and len(a) == 0 and len(b) == 0
    assert np.isclose(fourier_series_eval(a0, a, b, 3.0, 1.0), 5.0)


# ---- 6-11: discrete Fourier transform ----


def test_6_dft_matches_numpy_fft():
    x = _signal()
    np.testing.assert_allclose(dft(x), np.fft.fft(x), atol=1e-9)


def test_7_dft_of_a_complex_signal_matches_numpy_fft():
    rng = np.random.default_rng(1)
    x = rng.normal(size=16) + 1j * rng.normal(size=16)
    np.testing.assert_allclose(dft(x), np.fft.fft(x), atol=1e-9)


def test_8_inverse_undoes_the_transform():
    x = _signal(32, seed=2)
    np.testing.assert_allclose(inverse_dft(dft(x)).real, x, atol=1e-10)
    np.testing.assert_allclose(inverse_dft(dft(x)).imag, np.zeros(32), atol=1e-10)


def test_9_inverse_matches_numpy_ifft():
    spectrum = np.fft.fft(_signal(20, seed=3))
    np.testing.assert_allclose(inverse_dft(spectrum), np.fft.ifft(spectrum), atol=1e-10)


def test_10_special_cases_impulse_and_constant():
    impulse = np.zeros(8)
    impulse[0] = 1.0
    np.testing.assert_allclose(dft(impulse), np.ones(8), atol=1e-12)
    constant = dft(np.full(8, 3.0))
    np.testing.assert_allclose(constant, [24.0] + [0.0] * 7, atol=1e-10)


def test_11_real_signal_spectrum_is_conjugate_symmetric():
    spectrum = dft(_signal(16, seed=4))
    np.testing.assert_allclose(spectrum[1:], np.conj(spectrum[1:][::-1]), atol=1e-9)


# ---- 12-15: dominant frequency ----


def test_12_finds_a_pure_tone():
    rate = 64.0
    t = np.arange(64) / rate
    assert np.isclose(dominant_frequency(np.sin(2 * np.pi * 5 * t), rate), 5.0)


def test_13_ignores_a_large_constant_offset():
    rate = 100.0
    t = np.arange(100) / rate
    x = 50.0 + np.cos(2 * np.pi * 12 * t)
    assert np.isclose(dominant_frequency(x, rate), 12.0)


def test_14_picks_the_stronger_of_two_tones():
    rate = 128.0
    t = np.arange(128) / rate
    x = 0.5 * np.sin(2 * np.pi * 10 * t) + 2.0 * np.sin(2 * np.pi * 30 * t)
    assert np.isclose(dominant_frequency(x, rate), 30.0)


def test_15_frequency_scales_with_the_sample_rate():
    t = np.arange(40) / 40.0
    x = np.sin(2 * np.pi * 4 * t)
    assert np.isclose(dominant_frequency(x, 40.0), 4.0)
    assert np.isclose(dominant_frequency(x, 80.0), 8.0)
