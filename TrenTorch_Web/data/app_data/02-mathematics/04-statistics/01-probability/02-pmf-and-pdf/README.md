---
name: math-pmf-and-pdf
title: 'Probability Mass Functions and Probability Density Functions'
tags: [probability, foundations]
difficulty: Beginner
widget: distribution-shape-explorer
---

## Statement

### The problem, from first principles

`01-random-variables` introduced the PMF for a discrete random variable: a table of `P(X = x)` for each possible value. But most real quantities a model touches — a pixel value, an activation, a continuous latent variable — aren't discrete, and a PMF literally cannot describe them: for a continuous variable, the probability of hitting any _exact_ real number is zero (there are infinitely many of them to spread the probability over). A **probability density function (PDF)** solves this by describing probability as area under a curve instead of height at a point — `P(a <= X <= b)` is the integral of the density between `a` and `b`, not a single lookup. This question implements one canonical example of each: the discrete **Binomial** PMF (counting successes over `n` trials) and the continuous **Uniform** PDF (equally likely anywhere in an interval).

### From theory to code

Implement `binomial_pmf(n, p, k)`, returning `P(X = k)` for a `Binomial(n, p)` random variable, then `uniform_pdf(x, a, b)`, returning the constant density of a `Uniform(a, b)` random variable at point `x`. The signatures and docstrings are already in the editor.

### Constraints

- `n` is a positive integer, `k` is an integer in `[0, n]`, `p` is a float in `[0, 1]`.
- `a < b` for `uniform_pdf`; `x` can be any real number, including outside `[a, b]`.

### Hints

<details>
<summary>Hint 1</summary>

`binomial_pmf` is `C(n, k) * p**k * (1-p)**(n-k)` directly — `math.comb(n, k)` gives you the binomial coefficient without writing factorial by hand.

</details>

<details>
<summary>Hint 2</summary>

`uniform_pdf` is a single `if`: return `1 / (b - a)` when `a <= x <= b`, and `0.0` otherwise — the density is exactly constant everywhere inside the interval and exactly zero everywhere outside it.

</details>

## Theory

### The simple version

A PMF is a bar chart: each bar's _height_ directly tells you the probability of that exact outcome, and the heights add up to 1. A PDF is a skyline silhouette: no single point on the curve is a probability by itself (a density can even exceed 1) — only the _area_ under a stretch of the curve is a probability, and the total area under the whole curve is 1. The widget on this page lets you flip between the two: a Binomial bar chart on the left, a Uniform density's flat rectangle on the right — drag the sliders and watch the readout update.

### The formula

$$
P(X = k) = \binom{n}{k} p^k (1-p)^{n-k} \qquad \text{(Binomial PMF)}
$$

$$
f(x) = \begin{cases} \dfrac{1}{b-a} & a \leq x \leq b \\ 0 & \text{otherwise} \end{cases} \qquad \text{(Uniform PDF)}
$$

- `binom{n}{k}` — "n choose k," the number of distinct ways to pick which `k` of the `n` trials are the successes (see `03-combinatorics`, next in this track).
- `p^k (1-p)^{n-k}` — the probability of any _one specific_ ordering of `k` successes and `n-k` failures; multiplying by the count above accounts for every ordering that gives the same total.
- `f(x)` — the density function itself (lowercase `f`, distinct from the PMF's uppercase `P(X=k)`) — the notation difference is a deliberate signal that one is a probability and the other isn't.

### Why a PDF's value can exceed 1

A narrow Uniform interval, say `Uniform(0, 0.1)`, has density `1/0.1 = 10` everywhere inside it — clearly "more than 1," yet perfectly valid, because the total _area_ (`10 * 0.1 = 1`) is what has to equal 1, not the height. Drag the widget's `b` slider close to `a` and watch the rectangle grow tall and thin while its area — and the mean/variance readout — stays governed by the same interval.

### How NumPy/PyTorch actually implements this

`scipy.stats.binom.pmf(k, n, p)` computes exactly `binomial_pmf`, and `scipy.stats.uniform.pdf(x, loc=a, scale=b-a)` computes exactly `uniform_pdf` (SciPy's Uniform is parameterized by a start point and a width rather than two endpoints). `torch.distributions.Binomial(n, p).log_prob(k).exp()` and `torch.distributions.Uniform(a, b).log_prob(x).exp()` are the PyTorch equivalents, both working in log-space internally for numerical stability — the exact motivation behind the Numerical Computation track's log-sum-exp question.

<div class="tt-widget" data-widget="distribution-shape-explorer">
	<canvas id="dcanvas"></canvas>
	<div class="controls">
		<div class="btnrow">
			<button class="wbtn primary" id="discreteBtn" type="button">Discrete (PMF)</button>
			<button class="wbtn" id="continuousBtn" type="button">Continuous (PDF)</button>
		</div>
		<div class="ctrl" id="nCtrl">
			<label>Trials (n) <b id="nVal">10</b></label>
			<input type="range" id="nSlider" min="1" max="30" step="1" value="10" />
		</div>
		<div class="ctrl" id="pCtrl">
			<label>Success prob (p) <b id="pVal">0.50</b></label>
			<input type="range" id="pSlider" min="0" max="1" step="0.01" value="0.5" />
		</div>
		<div class="ctrl" id="aCtrl" style="display: none">
			<label>Lower bound (a) <b id="aVal">0.0</b></label>
			<input type="range" id="aSlider" min="-5" max="5" step="0.1" value="0" />
		</div>
		<div class="ctrl" id="bCtrl" style="display: none">
			<label>Upper bound (b) <b id="bVal">5.0</b></label>
			<input type="range" id="bSlider" min="-5" max="5" step="0.1" value="5" />
		</div>
		<div class="readout">
			<div>mean <b id="roMean">—</b></div>
			<div>variance <b id="roVar">—</b></div>
		</div>
	</div>
</div>

Flip between Discrete and Continuous mode and drag the sliders — notice the Binomial bars start to look bell-shaped as `n` grows, a preview of the Central Limit Theorem question later in `09-common-distributions`.

## Explanation

`binomial_pmf` calls `math.comb(n, k)` for the binomial coefficient, then multiplies by `p**k * (1-p)**(n-k)` — the probability of one specific arrangement of `k` successes and `n-k` failures, repeated once per arrangement via the coefficient. `uniform_pdf` is a plain `if a <= x <= b: return 1/(b-a); return 0.0` — the density is a step function, constant inside the interval and zero outside it, with no smoothing or interpolation at the boundary.
