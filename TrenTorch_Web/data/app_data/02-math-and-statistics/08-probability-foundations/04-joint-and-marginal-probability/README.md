---
name: math-joint-and-marginal-probability
title: 'Joint Probability and Marginalization'
tags: [probability, foundations]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Every question so far in this track has treated one random variable at a time. Real models almost never get that luxury: a classifier's output is a joint distribution over (predicted class, true class); a language model's training objective is a joint distribution over (every token in the sequence); a VAE's ELBO is built from a joint distribution over (data, latent code). **Joint probability**, `P(X=x, Y=y)`, is the probability that two random variables simultaneously take specific values — the natural generalization of a single PMF to a full table. **Marginalization** is the reverse operation: given the joint table, recover either variable's own PMF by summing the other one out — literally adding up a row or column and writing the total in the table's margin, which is where the name comes from.

### From theory to code

Implement `joint_from_independent(marginal_x, marginal_y)`, building a joint distribution table under the assumption that `X` and `Y` are independent, then `marginalize(joint, axis)`, recovering one variable's marginal PMF by summing the joint table over the other axis. The signatures and docstrings are already in the editor.

### Constraints

- `marginal_x` and `marginal_y` are 1D array-likes of non-negative floats that each sum to 1 (valid PMFs).
- `joint` is a 2D array-like where `joint[i, j] = P(X=x_i, Y=y_j)`.
- `axis` follows NumPy's own convention: it names the axis being summed _out_, not the one being kept.

### Hints

<details>
<summary>Hint 1</summary>

`joint_from_independent` is a single call to `np.outer(marginal_x, marginal_y)` — the outer product of two vectors produces exactly the "multiply every pair" table the independence formula asks for.

</details>

<details>
<summary>Hint 2</summary>

`marginalize` is `joint.sum(axis=axis)` — NumPy's own `axis` parameter already means "collapse this dimension by summing over it," which is precisely marginalization.

</details>

## Theory

### The simple version

Imagine a table with rows for "weather" (sunny/rainy) and columns for "commute mode" (bike/car), each cell holding the probability of that specific combination happening together — that whole table is the joint distribution. Add up an entire row and you get "the probability of that weather, regardless of commute mode" — you've marginalized commute mode away. Add up an entire column and you get "the probability of that commute mode, regardless of weather." The row and column totals, if you literally wrote them in the table's margins, are exactly the two variables' individual PMFs — hence "marginal" distribution.

### The formula

$$
P(X = x_i, Y = y_j) \quad \text{(joint)} \qquad P(X = x_i) = \sum_j P(X = x_i, Y = y_j) \quad \text{(marginal, via marginalization)}
$$

Independence is the special case where the joint has no extra structure beyond the two marginals:

$$
P(X = x_i, Y = y_j) = P(X = x_i) \cdot P(Y = y_j) \quad \text{if } X \perp Y
$$

- `P(X=x_i, Y=y_j)` — the joint probability, read "the probability that X equals x_i AND Y equals y_j simultaneously."
- `\sum_j` — sum over every possible value of `Y`, holding `X`'s value fixed at `x_i`; this is exactly what "summing a row" does in the table picture.
- `X \perp Y` — notation for "X is independent of Y" (formalized fully in `05-independence`, next in this track).

### Why marginalization always works, independent or not

Marginalization isn't an approximation or a special trick for independent variables — it follows directly from the law of total probability: `Y` must take _some_ value, so summing `P(X=x_i, Y=y_j)` over every possible `y_j` accounts for all the ways `X=x_i` could have happened, regardless of what `Y` did. This is why `marginalize` works identically whether or not the joint came from `joint_from_independent` — it's a property of any valid joint distribution.

### How NumPy/PyTorch actually implements this

`np.outer(a, b)` is the standard way to build an independence-structured joint table from two marginals, and `joint.sum(axis=0)` / `joint.sum(axis=1)` are literally how marginalization is done in practice — no dedicated "marginalize" function exists in NumPy or PyTorch because summing along an axis already _is_ the operation.

## Explanation

`joint_from_independent` converts both inputs to float NumPy arrays and returns `np.outer(marginal_x, marginal_y)`, whose `[i, j]` entry is `marginal_x[i] * marginal_y[j]` by definition of the outer product — exactly the independence formula. `marginalize` converts `joint` to a float array and returns `joint.sum(axis=axis)`, delegating directly to NumPy's own axis-reduction semantics rather than writing an explicit loop.
