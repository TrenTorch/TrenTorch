---
name: math-geometric-series
title: Geometric Series
tags: [calculus, series]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A geometric series adds up a list of numbers where each one is the previous one multiplied by the same fixed ratio: a bank balance that grows by 5% every year, a signal that loses half its strength at every step, a reward that is worth a little less with each step of delay. Adding the terms one by one works for a few terms, but it gives no way to answer the questions that matter: what is the total after a million terms, and does the total settle on a finite number if the list never ends? This question builds the closed forms that answer both.

### From theory to code

Implement `geometric_partial_sum(a, r, n)`, the sum of the first `n` terms, then `geometric_series_sum(a, r)`, the sum of the infinite series when it has one, then `terms_needed(a, r, tolerance)`, how many terms are needed before the partial sum is within `tolerance` of the infinite sum. The signatures and docstrings are already in the editor.

### Constraints

- `a` is the first term and `r` is the common ratio, both floats. The series is `a + a*r + a*r**2 + ...`.
- `geometric_partial_sum` takes an integer `n >= 0`. With `n = 0` there are no terms, so the sum is `0.0`. It must handle `r == 1` without dividing by zero, and it must not loop over the terms.
- `geometric_series_sum` only exists when `|r| < 1`. For any other ratio it raises `ValueError`.
- `terms_needed` requires `|r| < 1` and `tolerance > 0`, and returns the smallest integer `n >= 0` such that the gap between the infinite sum and the sum of the first `n` terms is below `tolerance`. If `a == 0` the answer is `0`.

### Hints

<details>
<summary>Hint 1</summary>

Multiply the partial sum by `r` and subtract it from the original. Almost every term cancels and a closed form is left, with `1 - r` in the denominator. That is also why `r == 1` needs its own case.

</details>

<details>
<summary>Hint 2</summary>

The gap between the infinite sum and the first `n` terms is the tail, which is itself a geometric series that starts at `a * r**n`. Its size has a closed form, so you can solve for `n` with a logarithm instead of testing values one at a time.

</details>

## Theory

### The simple version

Walk toward a wall by always covering half of the remaining distance. The steps are 1/2, then 1/4, then 1/8, and each is half the size of the one before. You never take an infinite number of steps in finite time, yet the total distance you cover creeps up toward exactly 1. A geometric series is any sum of this shape: when the steps shrink fast enough, infinitely many of them still add up to a finite number.

### The formula

The first `n` terms of $a + ar + ar^2 + \dots$ add up to

$$
S_n = \sum_{k=0}^{n-1} a r^k = a \, \frac{1 - r^n}{1 - r} \qquad (r \neq 1)
$$

and for `r = 1` every term is `a`, so $S_n = na$.

- Multiplying $S_n$ by $r$ shifts every term one place to the right. Subtracting leaves $S_n - rS_n = a - ar^n$, which solves to the formula above.
- When $|r| < 1$ the power $r^n$ shrinks to zero as $n$ grows, so the partial sums converge to

$$
S_\infty = \frac{a}{1 - r}
$$

- When $|r| \geq 1$ the terms do not shrink to zero, so the series has no finite sum.

### How many terms are enough

The error after `n` terms is the tail of the series:

$$
S_\infty - S_n = \frac{a\,r^n}{1 - r}
$$

Setting its absolute value below a tolerance $\varepsilon$ and taking logarithms gives

$$
n > \frac{\ln\left(\varepsilon\,|1 - r| / |a|\right)}{\ln |r|}
$$

The smaller $|r|$ is, the faster the series converges. A ratio close to 1 needs many terms.

### Where this shows up in machine learning

Reinforcement learning discounts future rewards by a factor $\gamma < 1$ per step. A reward of 1 at every step is worth $1 + \gamma + \gamma^2 + \dots = 1/(1 - \gamma)$ in total, which is why a discount factor keeps infinite-horizon returns finite. Learning-rate decay, exponential moving averages (where the weight on a value $k$ steps old is geometric) and momentum in optimizers are all geometric sequences in disguise.

### How NumPy/PyTorch actually implements this

Neither library has a geometric-series function, but `np.geomspace` generates the terms and `np.cumsum` of a `r ** np.arange(n)` array reproduces every partial sum at once. The closed form avoids that array entirely, which matters when `n` is large.

## Explanation

`geometric_partial_sum` returns `n * a` when `r` is exactly 1 (the closed form would divide by zero there) and `a * (1 - r**n) / (1 - r)` otherwise, so it does a constant amount of work no matter how large `n` is. `geometric_series_sum` rejects any ratio with `abs(r) >= 1` before applying `a / (1 - r)`, because for those ratios the formula returns a number that is not the sum of anything. `terms_needed` solves the tail inequality with a logarithm and rounds up with `ceil`; because the logarithm lands exactly on an integer at the boundary, it then checks the tail directly and adds one if the gap is not strictly below the tolerance, so the answer is the smallest `n` that really satisfies the requirement.
