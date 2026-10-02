---
name: math-joint-distributions-independence
title: 'Joint Distributions & Independence'
tags: [probability, foundations]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

**Joint & marginal probability**

Every question so far in this track has treated one random variable at a time. Real models almost never get that luxury: a classifier's output is a joint distribution over (predicted class, true class); a language model's training objective is a joint distribution over (every token in the sequence); a VAE's ELBO is built from a joint distribution over (data, latent code). **Joint probability**, `P(X=x, Y=y)`, is the probability that two random variables simultaneously take specific values, the natural generalization of a single PMF to a full table. **Marginalization** is the reverse operation: given the joint table, recover either variable's own PMF by summing the other one out, literally adding up a row or column and writing the total in the table's margin, which is where the name comes from.

**Independence**

`03-joint-independence` built joint distributions two ways: from the independence formula (`joint_from_independent`) and, implicitly, from any arbitrary table. This question makes that distinction operational: given _any_ joint distribution, how do you tell whether the two variables are actually independent, versus knowing one tells you something about the other? And when they're not independent, how do you compute the **conditional distribution**, "given that `Y` turned out to be a specific value, what's the updated distribution over `X`?" This is the single most-used probability operation in ML: a classifier literally _is_ a model of `P(\text{class} \mid \text{input})`, a conditional distribution.

### From theory to code

**Joint & marginal probability**

Implement `joint_from_independent(marginal_x, marginal_y)`, building a joint distribution table under the assumption that `X` and `Y` are independent, then `marginalize(joint, axis)`, recovering one variable's marginal PMF by summing the joint table over the other axis. The signatures and docstrings are already in the editor.

**Independence**

Implement `is_independent(joint, tol=1e-9)`, checking whether a joint distribution factorizes into the product of its own marginals, then `conditional_pmf_given_y(joint, y_index)`, computing `P(X \mid Y = y_index)`. The signatures and docstrings are already in the editor.

### Constraints

**Joint & marginal probability**

- `marginal_x` and `marginal_y` are 1D array-likes of non-negative floats that each sum to 1 (valid PMFs).
- `joint` is a 2D array-like where `joint[i, j] = P(X=x_i, Y=y_j)`.
- `axis` follows NumPy's own convention: it names the axis being summed _out_, not the one being kept.

**Independence**

- `joint` is a 2D array-like where `joint[i, j] = P(X=x_i, Y=y_j)`.
- `tol` is the absolute tolerance for the independence equality check (floating-point sums rarely match exactly).
- `y_index` always indexes a value of `Y` with non-zero marginal probability.

### Hints

**Joint & marginal probability**

<details>
<summary>Hint 1</summary>

`joint_from_independent` is a single call to `np.outer(marginal_x, marginal_y)`, the outer product of two vectors produces exactly the "multiply every pair" table the independence formula asks for.

</details>

<details>
<summary>Hint 2</summary>

`marginalize` is `joint.sum(axis=axis)`, NumPy's own `axis` parameter already means "collapse this dimension by summing over it," which is precisely marginalization.

</details>

**Independence**

<details>
<summary>Hint 1</summary>

`is_independent` needs both marginals first, `joint.sum(axis=1)` for `marginal_x`, `joint.sum(axis=0)` for `marginal_y` (same convention as `03-joint-independence`'s `marginalize`), then compares `joint` against `np.outer(marginal_x, marginal_y)` with `np.allclose`.

</details>

<details>
<summary>Hint 2</summary>

`conditional_pmf_given_y` is a single column of `joint` (`joint[:, y_index]`), divided by that column's total (`marginal_y[y_index]`) to renormalize it back into a valid PMF that sums to 1.

</details>

## Theory

### The simple version

**Joint & marginal probability**

Imagine a table with rows for "weather" (sunny/rainy) and columns for "commute mode" (bike/car), each cell holding the probability of that specific combination happening together, that whole table is the joint distribution. Add up an entire row and you get "the probability of that weather, regardless of commute mode", you've marginalized commute mode away. Add up an entire column and you get "the probability of that commute mode, regardless of weather." The row and column totals, if you literally wrote them in the table's margins, are exactly the two variables' individual PMFs, hence "marginal" distribution.

**Independence**

Two variables are independent if learning one tells you _nothing_ about the other: knowing today is rainy doesn't change your belief about a coin flip's outcome, rain and coin flips are independent. But knowing someone bought an umbrella today almost certainly _does_ update your belief about whether it's raining, purchase and weather are dependent. Conditioning is the formal version of "updating your belief": you take the slice of the joint table where `Y` equals the observed value, and renormalize that slice so it sums to 1 again (since you're now certain `Y` took that value, the remaining probability mass has to redistribute across `X`'s possibilities).

### The formula

**Joint & marginal probability**

$$
P(X = x_i, Y = y_j) \quad \text{(joint)} \qquad P(X = x_i) = \sum_j P(X = x_i, Y = y_j) \quad \text{(marginal, via marginalization)}
$$

Independence is the special case where the joint has no extra structure beyond the two marginals:

$$
P(X = x_i, Y = y_j) = P(X = x_i) \cdot P(Y = y_j) \quad \text{if } X \perp Y
$$

- `P(X=x_i, Y=y_j)`, the joint probability, read "the probability that X equals x_i AND Y equals y_j simultaneously."
- `\sum_j`, sum over every possible value of `Y`, holding `X`'s value fixed at `x_i`; this is exactly what "summing a row" does in the table picture.
- `X \perp Y`, notation for "X is independent of Y" (formalized fully in `03-joint-independence`, next in this track).

**Independence**

$$
X \perp Y \iff P(X=x_i, Y=y_j) = P(X=x_i)\,P(Y=y_j) \; \; \forall i, j
$$

$$
P(X = x_i \mid Y = y_j) = \frac{P(X = x_i, Y = y_j)}{P(Y = y_j)}
$$

- `X \perp Y`, "X is independent of Y"; the condition must hold for _every_ pair `(i, j)`, not just some.
- `P(X \mid Y=y_j)`, the conditional PMF; read the vertical bar as "given."
- The conditioning formula's denominator, `P(Y=y_j)`, is exactly the marginal that `03-joint-independence`'s `marginalize` computes.

### Why marginalization always works, independent or not

Marginalization isn't an approximation or a special trick for independent variables, it follows directly from the law of total probability: `Y` must take _some_ value, so summing `P(X=x_i, Y=y_j)` over every possible `y_j` accounts for all the ways `X=x_i` could have happened, regardless of what `Y` did. This is why `marginalize` works identically whether or not the joint came from `joint_from_independent`, it's a property of any valid joint distribution.

### Conditional independence, briefly

A related but distinct idea, `X \perp Y \mid Z`, says `X` and `Y` become independent _once you already know_ `Z`, dependence that was entirely explained by their shared relationship to `Z`. A classic example: shoe size and reading ability are correlated across a population (dependent), but that correlation vanishes once you condition on age (`Z`), within any single age group, shoe size tells you nothing extra about reading ability. This question's `is_independent` checks plain (unconditional) independence; extending it to check conditional independence would mean checking the same factorization separately within each slice of `Z`.

### Try it live

**Joint & marginal probability**

<div class="tt-widget" data-widget="math-joint-and-marginal-probability"></div>

**Independence**

<div class="tt-widget" data-widget="math-independence"></div>

### How NumPy/PyTorch actually implements this

**Joint & marginal probability**

`np.outer(a, b)` is the standard way to build an independence-structured joint table from two marginals, and `joint.sum(axis=0)` / `joint.sum(axis=1)` are literally how marginalization is done in practice, no dedicated "marginalize" function exists in NumPy or PyTorch because summing along an axis already _is_ the operation.

**Independence**

There's no dedicated "is independent" function in NumPy or PyTorch, checking it is exactly the `outer(marginals)` comparison this question implements by hand. Conditioning, however, is everywhere: `torch.nn.functional.softmax` followed by indexing a specific class _is_ evaluating a conditional PMF `P(\text{class} \mid \text{input})`, and `torch.distributions` objects generally expose `.log_prob(x)` for exactly this kind of query.

## Explanation

**Joint & marginal probability.** `joint_from_independent` converts both inputs to float NumPy arrays and returns `np.outer(marginal_x, marginal_y)`, whose `[i, j]` entry is `marginal_x[i] * marginal_y[j]` by definition of the outer product, exactly the independence formula. `marginalize` converts `joint` to a float array and returns `joint.sum(axis=axis)`, delegating directly to NumPy's own axis-reduction semantics rather than writing an explicit loop.

**Independence.** `is_independent` computes `marginal_x = joint.sum(axis=1)` and `marginal_y = joint.sum(axis=0)`, builds `expected = np.outer(marginal_x, marginal_y)`, the joint table `X` and `Y` _would_ have if independent, and returns `np.allclose(joint, expected, atol=tol)`, using a tolerance rather than exact equality since the marginals themselves are already sums of floats. `conditional_pmf_given_y` slices out column `y_index` (`joint[:, y_index]`, the joint probabilities of every `X` value paired with this specific `Y`) and divides by that column's own total (`marginal_y[y_index]`) to renormalize it into a distribution that sums to 1 on its own.
