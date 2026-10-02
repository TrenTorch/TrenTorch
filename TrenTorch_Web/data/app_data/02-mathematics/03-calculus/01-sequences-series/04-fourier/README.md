---
name: math-fourier-series-transforms
title: Fourier Series & Transforms
tags: [calculus, series, signals]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`02-taylor` approximates a function near one point by adding up powers of `x - a`. Fourier analysis approximates a function over a whole stretch by adding up waves instead: a repeating signal, however jagged, can be written as a sum of sines and cosines whose frequencies are whole multiples of a base frequency. The transform that finds those waves, and the inverse that rebuilds the signal from them, are among the most used algorithms in computing. This question builds both from their definitions, for a continuous periodic function (the series) and for a list of samples (the discrete transform).

### From theory to code

Implement `fourier_coefficients(f, period, num_terms, num_samples)` to find the cosine and sine weights of a periodic function, `fourier_series_eval(a0, a, b, period, t)` to rebuild the function from them, then `dft(x)` and `inverse_dft(spectrum)` for the discrete transform of a sample list, and `dominant_frequency(x, sample_rate)` to read the strongest frequency out of a signal. The signatures and docstrings are already in the editor.

### Constraints

- `f` takes a NumPy array of times and returns an array of the same shape. It repeats every `period`.
- `fourier_coefficients` estimates the integrals by averaging `f` at `num_samples` evenly spaced times over one period, starting at `t = 0`. It returns `(a0, a, b)` where `a` and `b` are arrays of length `num_terms` holding the weights for harmonics `1` through `num_terms`. The series is `a0 / 2 + sum(a[k-1] * cos(2*pi*k*t/period) + b[k-1] * sin(2*pi*k*t/period))`.
- `fourier_series_eval` accepts `t` as a float or an array and returns the same shape.
- `dft` and `inverse_dft` use the definition directly with a matrix of complex exponentials. They must not call `np.fft`. `dft` takes a 1D array of length `N` and returns a complex array of length `N`. `inverse_dft` returns a complex array that is the exact inverse.
- `dominant_frequency` returns the frequency in Hz of the largest-magnitude bin among frequencies from 1 bin up to the Nyquist bin, ignoring the zero-frequency (average) bin. `sample_rate` is in samples per second.

### Hints

<details>
<summary>Hint 1</summary>

Each weight is an average of `f(t)` multiplied by a cosine or sine of the matching frequency, times 2. Averaging over evenly spaced samples of one full period is the numerical stand-in for the integral.

</details>

<details>
<summary>Hint 2</summary>

Build the transform as one matrix: entry `(k, n)` is `exp(-2j * pi * k * n / N)`. Then `dft(x)` is a matrix-vector product, and the inverse uses the conjugate of the same matrix divided by `N`.

</details>

<details>
<summary>Hint 3</summary>

Bin `k` of an `N`-sample transform corresponds to a frequency of `k * sample_rate / N`. Only bins up to `N // 2` are independent for a real signal, since the rest mirror them.

</details>

## Theory

### The simple version

When a piano chord sounds, your ear hears one blended sound but you can still pick out the individual notes. Fourier analysis does that picking-out mathematically: it takes a blended signal and reports how much of each pure tone is inside it. Going the other way, mixing the right amount of each pure tone rebuilds the original signal exactly.

### The formula

A function with period $T$ can be written as

$$
f(t) = \frac{a_0}{2} + \sum_{k=1}^{\infty}\left[a_k \cos\frac{2\pi k t}{T} + b_k \sin\frac{2\pi k t}{T}\right]
$$

with weights found by integrating over one period:

$$
a_k = \frac{2}{T}\int_0^T f(t)\cos\frac{2\pi k t}{T}\,dt, \qquad b_k = \frac{2}{T}\int_0^T f(t)\sin\frac{2\pi k t}{T}\,dt
$$

- $a_0/2$ is the average value of the function.
- Each integral asks how strongly $f$ lines up with one pure wave. Waves of different whole-number frequencies are orthogonal, so each weight can be found independently of all the others.
- Truncating the sum at $K$ terms gives the best $K$-harmonic approximation in the least-squares sense. Jumps in $f$ make the approximation overshoot near the jump no matter how many terms are used.

### The discrete Fourier transform

A list of $N$ samples $x_0, \dots, x_{N-1}$ has the transform

$$
X_k = \sum_{n=0}^{N-1} x_n\, e^{-2\pi i k n / N}, \qquad x_n = \frac{1}{N}\sum_{k=0}^{N-1} X_k\, e^{2\pi i k n / N}
$$

The complex exponential packs a cosine and a sine into one term, since $e^{i\theta} = \cos\theta + i\sin\theta$. The magnitude $|X_k|$ says how much of frequency $k$ cycles per window is present, and the angle of $X_k$ says where in its cycle that wave starts.

- Bin $k$ corresponds to the frequency $k \cdot f_s / N$ Hz when samples arrive $f_s$ times per second.
- For a real signal, bin $N-k$ is the complex conjugate of bin $k$, so only bins $0$ through $N/2$ carry independent information. Frequencies above $f_s/2$ (the **Nyquist frequency**) cannot be told apart from lower ones.
- Computing every bin directly takes $N^2$ multiplications. The fast Fourier transform produces the same numbers in $N \log N$ steps.

### Where this shows up in machine learning

Convolution in the time domain is multiplication in the frequency domain, which is how large convolutions are computed quickly. Audio models start from spectrograms, which are transforms of short windows. Positional encodings in transformers are sines and cosines at geometrically spaced frequencies, a Fourier-style basis for position. Spectral methods on graphs and random Fourier features for kernel approximation rest on the same orthogonality.

### How NumPy/PyTorch actually implements this

`np.fft.fft` and `torch.fft.fft` compute the transform above with the fast algorithm, and `np.fft.ifft` is the inverse. `np.fft.rfft` keeps only the non-mirrored half for real signals, and `np.fft.fftfreq(n, d=1/sample_rate)` gives the frequency of every bin. They agree with the matrix version to floating point error, which is exactly what the tests check.

## Explanation

`fourier_coefficients` samples `f` at `num_samples` evenly spaced times across one period, then takes `2 * mean(f * cos(...))` and `2 * mean(f * sin(...))` for each harmonic with one broadcasted matrix of angles. Averaging over a full period at uniform spacing is exact for any wave whose frequency is below half the sampling density, so a trigonometric polynomial is recovered to rounding error. `fourier_series_eval` is the series formula with `np.asarray` on the input so a scalar and an array both work. `dft` builds the matrix of `exp(-2j * pi * k * n / N)` from an outer product of the index range with itself and applies it to `x`, and `inverse_dft` applies the conjugate matrix and divides by `N`, which undoes it exactly because the rows are orthogonal. `dominant_frequency` takes magnitudes of the transform, looks only at bins `1` through `N // 2` to skip the average and the mirrored half, and converts the winning bin index to Hz with `k * sample_rate / N`.
