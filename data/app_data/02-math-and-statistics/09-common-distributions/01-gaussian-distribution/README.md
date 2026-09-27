---
name: math-probability-gaussian-distribution
title: 'Gaussian Distribution: the bell curve behind noise, errors, and the CLT'
tags: [probability, distributions]
difficulty: Intermediate
widget: gaussian-distribution
---

## Statement

### The problem, from first principles

Most naturally occurring measurement noise — sensor error, rounding error, the sum of many small independent effects — piles up into the same recognizable shape: symmetric, peaked at the average, thinning out fast at the extremes. That shape is the Gaussian, and it is not a coincidence it shows up everywhere; the Central Limit Theorem explains exactly why.

Here you'll implement the Gaussian's probability density function directly from its formula, then generate actual Gaussian-distributed samples from nothing but uniform random numbers using the **Box-Muller transform** — the concrete answer to "where does randomness with this specific shape actually come from."

### From theory to code

Implement `gaussian_pdf(x, mu, sigma)` against the closed-form density in Theory, then `sample_gaussian(mu, sigma, n, uniform_draws)`, which turns pairs of uniform random draws into Gaussian samples via Box-Muller. The signatures and docstrings are already in the editor.

### Constraints

- `sigma > 0` (a zero or negative standard deviation is undefined).
- `x` may be a scalar or a NumPy array of any shape.
- `uniform_draws` are pre-generated floats in `[0, 1)`, exactly `2 * n` of them, so results are deterministic and checkable.
- Return samples as a flat array of length `n`.

### Hints

<details>
<summary>Hint 1</summary>

Box-Muller turns _two_ uniform draws `u1, u2` into _two_ independent standard-normal samples at once — you'll use `n/2` pairs (rounded up) to get `n` samples.

</details>

<details>
<summary>Hint 2</summary>

A standard-normal sample `z` (μ=0, σ=1) becomes a general Gaussian sample via `x = mu + sigma * z` — generate standard-normal first, then shift/scale.

</details>

## Theory

### The simple version

Imagine measuring the height of every adult in a city. Most people cluster near the average; a few are noticeably shorter or taller; almost nobody is 3 feet or 8 feet tall. Plot a histogram of enough people and you get this exact bell shape — narrow and tall if the population is homogeneous (small σ), wide and flat if it's diverse (large σ), but always centered on the average (μ) and always symmetric.

### The formula

$$
f(x) = \frac{1}{\sigma\sqrt{2\pi}} \exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)
$$

- `μ` — the mean, where the curve is centered and peaks.
- `σ` — the standard deviation, how spread out the curve is.
- `σ²` — the variance, σ squared, appears directly in the exponent.
- `f(x)` — probability _density_ at `x`, not a probability itself; the area under the curve is.

The `1/(σ√2π)` term out front exists purely to make the total area under the curve equal exactly 1, as any valid probability density must — the exponential shape is what makes it a bell; the front term is just the normalizer.

### Try it live

<div class="tt-widget" data-widget="gaussian-distribution">
	<canvas id="gcanvas"></canvas>
	<div class="controls">
		<div class="ctrl">
			<label>Mean (μ) <b id="muVal">0.0</b></label>
			<input type="range" id="muSlider" min="-4" max="4" step="0.1" value="0" />
		</div>
		<div class="ctrl">
			<label>Std. dev (σ) <b id="sigmaVal">1.0</b></label>
			<input type="range" id="sigmaSlider" min="0.3" max="3" step="0.1" value="1" />
		</div>
		<div class="btnrow">
			<button class="wbtn primary" id="drawBtn" type="button">Draw 500 samples</button>
			<button class="wbtn" id="resetBtn" type="button">Reset</button>
		</div>
		<div class="readout">
			<div>μ <b id="roMu">0.00</b></div>
			<div>σ <b id="roSigma">1.00</b></div>
			<div>samples drawn <b id="roN">0</b></div>
			<div>sample mean <b id="roMean">—</b></div>
			<div>sample std <b id="roStd">—</b></div>
		</div>
	</div>
</div>

Drag μ and σ to reshape the curve, then draw samples and watch the histogram converge onto it as the sample count grows.

### How NumPy/PyTorch actually implements this

`np.random.normal(mu, sigma, n)` and `torch.randn(n) * sigma + mu` both use a faster variant of the same idea (the Ziggurat algorithm, not literal Box-Muller) for performance, but the underlying guarantee is identical: turn uniform randomness into Gaussian-shaped randomness. The PDF formula above is what `scipy.stats.norm.pdf` and `torch.distributions.Normal(mu, sigma).log_prob(x).exp()` compute directly.

## Explanation

`gaussian_pdf` evaluates the closed-form density directly: a normalizing coefficient `1/(σ√2π)` times `exp` of the negative squared distance from the mean, scaled by `2σ²`. `sample_gaussian` consumes uniform draws in pairs and produces standard-normal samples in pairs (`z0, z1`) via Box-Muller, generating in batches of two and only slicing down to `n` at the very end — trying to generate exactly `n` one at a time would throw away half of every pair's information for free. Clipping `u1` away from exactly `0` avoids `log(0) = -inf`, which would otherwise make the radius blow up.
