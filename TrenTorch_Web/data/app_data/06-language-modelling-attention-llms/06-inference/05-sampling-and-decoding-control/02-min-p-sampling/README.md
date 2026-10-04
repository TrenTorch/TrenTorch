---
name: lm-min-p-sampling
title: Min-p Sampling
tags: [decoding, sampling, min-p]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Top-p chooses a fixed probability _mass_, which can keep many junk tokens when the distribution is flat and cut good options when it is peaked at high temperature. **Min-p** instead sets a threshold _relative to the best token_: keep every token whose probability is at least `min_p` times the probability of the most likely token. If the top token has probability 0.8 and `min_p = 0.1`, the cutoff is 0.08. If the model is unsure and the top token has 0.2, the cutoff drops to 0.02. The candidate set therefore scales with the model's confidence, and the rule stays sensible when the temperature is raised for creativity.

### From theory to code

Implement `min_p_filter`.

### Constraints

- `probs` is a 1-D probability vector and `0 <= min_p <= 1`.
- The threshold is `min_p * probs.max()`. Keep every token with `probs >= threshold` (so the top token is always kept).
- Zero all others and renormalize so the result sums to 1. Do not modify `probs`.

### Hints

<details>
<summary>Hint 1</summary>

A boolean mask `probs >= min_p * probs.max()` does the work.

</details>

<details>
<summary>Hint 2</summary>

With `min_p = 0` nothing is removed, with `min_p = 1` only the maximum (and exact ties) remains.

</details>

## Theory

### The simple version

Judging candidates relative to the front-runner: if the leader is far ahead, only a close second is worth considering; if the field is tight, nearly everyone qualifies.

### The formula

$$
\text{keep } i \iff p_i \ge \rho\,\max_j p_j, \qquad
\tilde p_i = \frac{p_i\,\mathbf{1}[\text{keep}]}{\sum_j p_j\,\mathbf{1}[\text{keep}]}
$$

### How this is done in practice

Min-p is available in `llama.cpp`, vLLM and Hugging Face generation configs. It is usually applied after temperature scaling, which is exactly where it is more robust than top-p.

## Explanation

A threshold relative to the maximum is a single comparison. The tests contrast it with an absolute cutoff to show the adaptation to confidence.
