import numpy as np


def fourier_coefficients(f, period, num_terms, num_samples=1024):
    """
    f: function taking a NumPy array of times, returning an array of the
        same shape; repeats every `period`
    period: the period of f (float > 0)
    num_terms: how many harmonics to compute (int >= 0)
    num_samples: evenly spaced times over one period, starting at t = 0

    Returns:
        (a0, a, b): a0 is a float and a, b are 1D arrays of length
        num_terms, so that f(t) is approximately
        a0/2 + sum(a[k-1]*cos(2*pi*k*t/period) + b[k-1]*sin(2*pi*k*t/period)).
    """
    # TODO: Estimate each integral from Theory by averaging over the samples.
    pass


def fourier_series_eval(a0, a, b, period, t):
    """
    a0, a, b: as returned by fourier_coefficients
    period: the period of the function
    t: a float or a NumPy array of times

    Returns:
        The value of the series at t, with the same shape as t.
    """
    # TODO: Implement the series formula from Theory.
    pass


def dft(x):
    """
    x: 1D array-like of N samples

    Returns:
        The discrete Fourier transform of x as a complex array of length N,
        computed directly from the definition. Do not use np.fft.
    """
    # TODO: Build the matrix of complex exponentials from Theory.
    pass


def inverse_dft(spectrum):
    """
    spectrum: 1D complex array of length N, as returned by dft

    Returns:
        The inverse transform as a complex array of length N, computed
        directly from the definition. Do not use np.fft.
    """
    # TODO: Use the conjugate of the same matrix, scaled as in Theory.
    pass


def dominant_frequency(x, sample_rate):
    """
    x: 1D real array of N samples
    sample_rate: samples per second (float > 0)

    Returns:
        The frequency in Hz of the strongest bin among bins 1 .. N // 2,
        ignoring the zero-frequency bin, as a float.
    """
    # TODO: Use dft and the bin-to-frequency rule from Theory.
    pass
