---
name: math-entropy
title: Entropy of a discrete distribution
tags: [information-theory]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A coin that's guaranteed to land heads tells you nothing new when you flip it, you already knew the answer. A fair coin, by contrast, is maximally surprising every single flip, you genuinely can't predict it. Entropy is the precise, quantitative version of "how surprising is this distribution, on average," and it's measured in **bits**: the number of yes/no questions you'd need, on average, to pin down an outcome drawn from that distribution.

This isn't an abstract curiosity: `02-cross-entropy` (Deep Learning Core) is named "cross"-entropy specifically because it's a close cousin of this exact quantity, and understanding entropy first makes cross-entropy's formula, and why it measures "how surprised the model was by the true answer," make actual sense rather than being a formula to memorize.

### From theory to code

Theory gives the exact entropy formula, `-sum(p * log(p))`, and flags a numerical edge case: `log(0)` is `-inf`, but `p * log(p)` should be treated as exactly `0` when `p = 0` (a zero-probability outcome contributes nothing to the average surprise, since it never happens).

Implement `entropy(probs, base=2.0)` against that reasoning. The signature and docstring are already in the editor.

### Constraints

- `probs` is a valid probability distribution (non-negative, sums to `1`).
- Clip probabilities before taking a log, don't let `log(0)` produce `nan` or crash.
- `base` controls the unit: `base=2` gives bits (the default), `base=np.e` gives nats.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.clip(probs, eps, 1.0)` keeps every probability comfortably away from exactly `0` before you take its log.

</details>

<details>
<summary>Hint 2</summary>

Changing `base` is a single division at the end: divide the natural-log-based sum by `log(base)` (a general change-of-base rule).

</details>

## Theory

### The simple version

Imagine playing 20 Questions. If the answer is always "yes" (a certain outcome), you need zero questions, you already knew. If the answer is a coin flip with no useful clues, you need exactly one well-chosen yes/no question, on average, to nail it down. If there are 4 equally likely possibilities, you need 2 questions (binary search: "is it in the first half? is it in the first quarter or the second?"). Entropy IS that expected number of questions, and it grows exactly with how "spread out" and unpredictable a distribution is.

### The formula

Shannon entropy of a discrete probability distribution:

```text
H(P) = -sum_i(p_i * log_base(p_i))
```

`base=2` (bits) is the standard convention: a distribution over `n` equally likely outcomes has entropy exactly `log2(n)` bits (a fair coin: `log2(2) = 1` bit; a fair 4-sided die: `log2(4) = 2` bits). A distribution concentrated entirely on one outcome (probability `1` for one value, `0` for everything else) has entropy exactly `0`, no surprise, no information gained by observing it. Entropy is maximized by the uniform distribution over a fixed set of outcomes, and that maximum grows with how many outcomes there are, more possibilities means more potential surprise.

The `p_i = 0` edge case matters: `log(0)` is `-infinity`, but the actual quantity being computed, `p_i * log(p_i)`, has a well-defined limit of `0` as `p_i -> 0` (an event that never happens contributes nothing to the average surprise). Clipping probabilities away from exactly `0` before taking the log sidesteps computing `0 * -inf` (which floating point evaluates as `nan`, not `0`) while still landing on the mathematically correct answer.

### How PyTorch actually implements this

`torch.distributions.Categorical(probs).entropy()` computes exactly this formula, and it's used directly in reinforcement learning (an entropy bonus is added to many policy-gradient losses specifically to discourage the policy from collapsing to a single, overconfident action too early, encouraging continued exploration, this shows up explicitly in the RL & Alignment part of this curriculum). More broadly, entropy is the "zero" against which `02-cross-entropy`'s cross-entropy and `03-kl-divergence`'s (next question) KL divergence are both defined: cross-entropy is "how many bits does it ACTUALLY take to encode outcomes from the true distribution, using a code built for a DIFFERENT (predicted) distribution," and it's never smaller than the true distribution's own entropy, the gap between them is exactly KL divergence.

## Explanation

`entropy` clips `probs` away from exactly `0` (using `_EPS` as the floor) before taking the log, so `log(0)` never occurs, then computes `-sum(probs * log(clipped))`, using the ORIGINAL (unclipped) `probs` as the multiplying factor: since a genuinely-zero `probs[i]` makes the whole term `0` regardless of how large `log(clipped[i])` is in magnitude, the clip only protects the log call itself, not the final sum. Dividing by `log(base)` converts from natural log (nats) to whatever unit `base` specifies (bits, by default).
