---
name: math-independence
title: 'Independence and Conditional Probability'
tags: [probability, foundations]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`04-joint-and-marginal-probability` built joint distributions two ways: from the independence formula (`joint_from_independent`) and, implicitly, from any arbitrary table. This question makes that distinction operational: given _any_ joint distribution, how do you tell whether the two variables are actually independent, versus knowing one tells you something about the other? And when they're not independent, how do you compute the **conditional distribution** — "given that `Y` turned out to be a specific value, what's the updated distribution over `X`?" This is the single most-used probability operation in ML: a classifier literally _is_ a model of `P(\text{class} \mid \text{input})`, a conditional distribution.

### From theory to code

Implement `is_independent(joint, tol=1e-9)`, checking whether a joint distribution factorizes into the product of its own marginals, then `conditional_pmf_given_y(joint, y_index)`, computing `P(X \mid Y = y_index)`. The signatures and docstrings are already in the editor.

### Constraints

- `joint` is a 2D array-like where `joint[i, j] = P(X=x_i, Y=y_j)`.
- `tol` is the absolute tolerance for the independence equality check (floating-point sums rarely match exactly).
- `y_index` always indexes a value of `Y` with non-zero marginal probability.

### Hints

<details>
<summary>Hint 1</summary>

`is_independent` needs both marginals first — `joint.sum(axis=1)` for `marginal_x`, `joint.sum(axis=0)` for `marginal_y` (same convention as `04-joint-and-marginal-probability`'s `marginalize`) — then compares `joint` against `np.outer(marginal_x, marginal_y)` with `np.allclose`.

</details>

<details>
<summary>Hint 2</summary>

`conditional_pmf_given_y` is a single column of `joint` (`joint[:, y_index]`), divided by that column's total (`marginal_y[y_index]`) to renormalize it back into a valid PMF that sums to 1.

</details>

## Theory

### The simple version

Two variables are independent if learning one tells you _nothing_ about the other: knowing today is rainy doesn't change your belief about a coin flip's outcome — rain and coin flips are independent. But knowing someone bought an umbrella today almost certainly _does_ update your belief about whether it's raining — purchase and weather are dependent. Conditioning is the formal version of "updating your belief": you take the slice of the joint table where `Y` equals the observed value, and renormalize that slice so it sums to 1 again (since you're now certain `Y` took that value, the remaining probability mass has to redistribute across `X`'s possibilities).

### The formula

$$
X \perp Y \iff P(X=x_i, Y=y_j) = P(X=x_i)\,P(Y=y_j) \; \; \forall i, j
$$

$$
P(X = x_i \mid Y = y_j) = \frac{P(X = x_i, Y = y_j)}{P(Y = y_j)}
$$

- `X \perp Y` — "X is independent of Y"; the condition must hold for _every_ pair `(i, j)`, not just some.
- `P(X \mid Y=y_j)` — the conditional PMF; read the vertical bar as "given."
- The conditioning formula's denominator, `P(Y=y_j)`, is exactly the marginal that `04-joint-and-marginal-probability`'s `marginalize` computes.

### Conditional independence, briefly

A related but distinct idea, `X \perp Y \mid Z`, says `X` and `Y` become independent _once you already know_ `Z` — dependence that was entirely explained by their shared relationship to `Z`. A classic example: shoe size and reading ability are correlated across a population (dependent), but that correlation vanishes once you condition on age (`Z`) — within any single age group, shoe size tells you nothing extra about reading ability. This question's `is_independent` checks plain (unconditional) independence; extending it to check conditional independence would mean checking the same factorization separately within each slice of `Z`.

### How NumPy/PyTorch actually implements this

There's no dedicated "is independent" function in NumPy or PyTorch — checking it is exactly the `outer(marginals)` comparison this question implements by hand. Conditioning, however, is everywhere: `torch.nn.functional.softmax` followed by indexing a specific class _is_ evaluating a conditional PMF `P(\text{class} \mid \text{input})`, and `torch.distributions` objects generally expose `.log_prob(x)` for exactly this kind of query.

## Explanation

`is_independent` computes `marginal_x = joint.sum(axis=1)` and `marginal_y = joint.sum(axis=0)`, builds `expected = np.outer(marginal_x, marginal_y)` — the joint table `X` and `Y` _would_ have if independent — and returns `np.allclose(joint, expected, atol=tol)`, using a tolerance rather than exact equality since the marginals themselves are already sums of floats. `conditional_pmf_given_y` slices out column `y_index` (`joint[:, y_index]`, the joint probabilities of every `X` value paired with this specific `Y`) and divides by that column's own total (`marginal_y[y_index]`) to renormalize it into a distribution that sums to 1 on its own.
