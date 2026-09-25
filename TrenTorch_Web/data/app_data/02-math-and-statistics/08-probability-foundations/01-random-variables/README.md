---
name: math-random-variables
title: 'Random Variables: Discrete vs. Continuous'
tags: [probability, foundations]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Every ML model that outputs a probability — a classifier's softmax, a language model's next-token distribution, a VAE's latent code — is treating some quantity as a **random variable**: a variable whose value isn't fixed, but drawn from a distribution. A **discrete** random variable takes one of a countable set of values (a class label, a token id, a die roll); its distribution is a **probability mass function (PMF)**, a table of `P(X = x)` for each possible `x`. A **continuous** random variable takes any value in a range (a pixel intensity, a sensor reading); it doesn't have a PMF at all — a single exact value has probability zero — instead it has a **probability density function (PDF)**, covered in the next question (`02-pmf-and-pdf`). This question stays entirely in the discrete case and nails down the two things every valid PMF must satisfy, plus the single most useful summary of a random variable: its **expected value**.

### From theory to code

Implement `is_valid_pmf(probabilities)`, checking the two axioms every PMF must satisfy, then `expected_value_discrete(outcomes, probabilities)`, computing `E[X]`. The signatures and docstrings are already in the editor.

### Constraints

- `probabilities` is a list/tuple of floats.
- `outcomes` and `probabilities` are the same length, and `probabilities[i]` is `P(X = outcomes[i])`.
- "Sums to 1" means within `1e-9` of exactly 1, to tolerate floating-point roundoff.

### Hints

<details>
<summary>Hint 1</summary>

`is_valid_pmf` checks two separate conditions and both must hold: every probability is `>= 0`, and they sum to (approximately) `1`.

</details>

<details>
<summary>Hint 2</summary>

`expected_value_discrete` is a single weighted sum — pair each outcome with its probability and add up `outcome * probability`, exactly what the formula in Theory says.

</details>

## Theory

### The simple version

Think of a random variable as a vending machine: you press a button (run the experiment), and it dispenses one of several items (a value), but which item comes out is governed by fixed odds printed on the machine (the distribution). For a **discrete** random variable, those odds are a finite or countably infinite list: "30% chance of a cola, 70% chance of water." A PMF is exactly that printed list, formalized: a function from each possible outcome to its probability.

### The formula

$$
\sum_{i} P(X = x_i) = 1, \qquad P(X = x_i) \geq 0 \; \forall i
$$

$$
E[X] = \sum_{i} x_i \cdot P(X = x_i)
$$

- `X` — the random variable itself (the vending machine), as distinct from `x_i`, one of its possible _values_ (an item it could dispense).
- `P(X = x_i)` — the probability of that specific outcome; this whole function of `x_i` is the PMF.
- `E[X]` — "expected value" or "expectation," the probability-weighted average of every possible outcome — not necessarily a value `X` can actually take (a fair die's `E[X] = 3.5`, which no roll ever produces).

### Why both axioms matter

Non-negativity (`P(X = x_i) >= 0`) is required because probability is a measure of likelihood — a "negative chance" of something happening isn't a coherent concept, and downstream code that treats a PMF as if it were, say, a softmax output would silently produce nonsense if this were violated. Summing to 1 encodes "something in the outcome set is guaranteed to happen" — the outcome set is exhaustive by construction, so the total probability mass across all of it has nowhere else to go.

### How NumPy/PyTorch actually implements this

`np.random.choice(outcomes, p=probabilities)` draws a single sample from exactly this kind of discrete random variable, and NumPy internally validates that `p` sums to 1 (raising `ValueError` if it doesn't) — the same check `is_valid_pmf` performs by hand here. `torch.distributions.Categorical(probs=probabilities)` does the same for PyTorch, and its `.mean` when outcomes are `0..n-1` is exactly `expected_value_discrete`.

## Explanation

`is_valid_pmf` uses Python's `all()` to check non-negativity across every probability in one pass, `and`-ed with a tolerance check (`abs(sum(probabilities) - 1.0) < 1e-9`) rather than exact equality, since summing floats rarely lands on exactly `1.0`. `expected_value_discrete` pairs `outcomes` and `probabilities` element-wise with `zip` and sums `o * p` for each pair — the direct, one-line translation of `E[X] = Σ x_i P(X=x_i)` into code.
