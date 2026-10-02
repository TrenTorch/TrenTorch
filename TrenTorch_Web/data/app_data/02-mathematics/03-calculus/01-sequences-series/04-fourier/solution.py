import numpy as np


def fourier_coefficients(f, period, num_terms, num_samples=1024):
    t = np.arange(num_samples) * period / num_samples
    values = np.asarray(f(t), dtype=float)
    harmonics = np.arange(1, num_terms + 1)
    angles = 2.0 * np.pi * np.outer(harmonics, t) / period
    a0 = float(2.0 * values.mean())
    a = 2.0 * (np.cos(angles) * values).mean(axis=1)
    b = 2.0 * (np.sin(angles) * values).mean(axis=1)
    return a0, a, b


def fourier_series_eval(a0, a, b, period, t):
    t = np.asarray(t, dtype=float)
    result = np.full(t.shape, a0 / 2.0)
    for k, (a_k, b_k) in enumerate(zip(a, b), start=1):
        angle = 2.0 * np.pi * k * t / period
        result = result + a_k * np.cos(angle) + b_k * np.sin(angle)
    return result if result.ndim else float(result)


def _dft_matrix(n, sign):
    k = np.arange(n)
    return np.exp(sign * 2j * np.pi * np.outer(k, k) / n)


def dft(x):
    x = np.asarray(x, dtype=complex)
    return _dft_matrix(len(x), -1) @ x


def inverse_dft(spectrum):
    spectrum = np.asarray(spectrum, dtype=complex)
    return _dft_matrix(len(spectrum), 1) @ spectrum / len(spectrum)


def dominant_frequency(x, sample_rate):
    n = len(x)
    magnitudes = np.abs(dft(x))[1 : n // 2 + 1]
    return float((np.argmax(magnitudes) + 1) * sample_rate / n)
