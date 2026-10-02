---
name: math-chain-rule-of-probability
title: 'The Chain Rule of Conditional Probability'
tags: [probability, foundations]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

**Naming collision, worth stating up front:** this "chain rule" has nothing to do with calculus's chain rule for differentiating composed functions — it's an unrelated rule that happens to share a name, because both describe "a chain of dependent steps multiplied together." Here, the chain rule of probability answers a very practical question: how do you compute the joint probability of several variables when you only know a chain of _conditional_ probabilities — `P(X)`, then `P(Y | X)`, then `P(Z | X, Y)`, and so on? This is exactly how autoregressive language models define the probability of an entire sequence: `P(\text{token}_1) \cdot P(\text{token}_2 \mid \text{token}_1) \cdot P(\text{token}_3 \mid \text{token}_1, \text{token}_2) \cdots` — each token's probability conditioned on every token before it, multiplied together into one number for the whole sequence.

### From theory to code

Implement `joint_via_chain_rule(p_x, p_y_given_x, p_z_given_xy)` for the three-variable case, then `chain_rule_general(conditionals)`, generalizing to any number of variables given as a list of conditional-probability factors. The signatures and docstrings are already in the editor.

### Constraints

- All probability arguments are floats in `[0, 1]`.
- `conditionals` is a non-empty list; its first entry is an unconditional probability, every entry after that is conditioned on all variables before it in the list's order.

### Hints

<details>
<summary>Hint 1</summary>

`joint_via_chain_rule` is a single multiplication of its three arguments — no conditioning logic to implement, since each argument is already the correctly-conditioned probability.

</details>

<details>
<summary>Hint 2</summary>

`chain_rule_general` is `math.prod(conditionals)` — Python's `math.prod` multiplies every element of an iterable together, which is exactly what an arbitrary-length chain rule needs.

</details>

## Theory

### The simple version

Think of drawing colored balls from a bag, one at a time, without replacement, and asking for the probability of a specific sequence of colors. The probability of the _first_ ball being red is unconditional. The probability of the _second_ ball being blue depends on what the first ball was (since it's not replaced, it changed the bag's contents) — that's `P(\text{2nd blue} \mid \text{1st red})`. The probability of the whole sequence happening is the product of each step's probability, conditioned on everything drawn before it — you never need the true unconditional probability of "2nd ball blue," only its probability _given_ the specific history that already happened.

### The formula

$$
P(X, Y, Z) = P(X) \cdot P(Y \mid X) \cdot P(Z \mid X, Y)
$$

$$
P(X_1, X_2, \ldots, X_n) = \prod_{i=1}^{n} P\bigl(X_i \mid X_1, \ldots, X_{i-1}\bigr)
$$

- `P(X, Y, Z)` — the joint probability of all three variables taking their specific values simultaneously (same notation as `04-joint-and-marginal-probability`, extended to three variables).
- `P(Y \mid X)` — the conditional probability of `Y`, given that `X`'s value is already known (from `05-independence`).
- `\prod_{i=1}^{n}` — product notation from `00-notation-and-foundations/02-product-notation`; each factor conditions on every variable that came before it in the chosen ordering.

### Why any ordering of the variables works

The chain rule holds for _every_ ordering of the variables, not just one — `P(X,Y,Z) = P(Z) \cdot P(Y \mid Z) \cdot P(X \mid Y, Z)` is equally valid. It follows directly from repeatedly applying the definition of conditional probability, `P(A \mid B) = P(A, B) / P(B)`, rearranged to `P(A, B) = P(B) \cdot P(A \mid B)`, one variable at a time. Which ordering is most useful depends entirely on which conditionals are easiest to model or estimate for the problem at hand — autoregressive language models pick the left-to-right token order because it matches how text is generated and read.

### How NumPy/PyTorch actually implements this

An autoregressive model (any GPT-style language model) computes exactly `chain_rule_general`'s product at training time, though almost always in log-space (summing `log P(X_i \mid X_{<i})` instead of multiplying raw probabilities) to avoid the underflow the Numerical Computation track's floating-point question covers — `torch.nn.functional.cross_entropy` applied per-token and summed over the sequence _is_ the negative log of this chain-rule product.

## Explanation

`joint_via_chain_rule` returns `p_x * p_y_given_x * p_z_given_xy` — a direct three-factor multiplication, since each argument is already the correctly-conditioned probability and no further conditioning computation is needed. `chain_rule_general` returns `math.prod(conditionals)`, generalizing the same multiplication to an arbitrary-length list without hand-writing a loop or an explicit accumulator.
