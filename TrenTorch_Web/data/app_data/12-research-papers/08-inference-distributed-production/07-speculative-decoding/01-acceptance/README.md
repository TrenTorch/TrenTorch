---
name: research-spec-acceptance
title: 'Speculative Decoding: The Acceptance Probability'
tags: [research-papers, systems, inference, decoding]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Speculative decoding (Leviathan et al., 2023) lets a small draft model propose several tokens, which the large target model checks in one parallel pass. A drafted token is accepted with probability min(1, p over q), which keeps the output distribution exactly that of the target model.

### From theory to code

Implement `acceptance_prob(p, q)`, the acceptance probability of one drafted token.

### Constraints

- Probabilities are in (0, 1].

### Hints

<details>
<summary>Hint 1</summary>

Divide the target probability by the draft probability and cap the result at one.

</details>

## Theory

### The simple version

Accepting by this ratio corrects for the draft's bias, so the final samples follow the target distribution even though a cheaper model did the drafting.

### The formula

$$\alpha = \min\!\left(1, \frac{p(x)}{q(x)}\right)$$

### How NumPy/PyTorch actually implements this

Inference servers implement this check per drafted token after one batched target forward pass.

## Explanation

The rule is the standard rejection-sampling correction; rejected tokens are resampled from the residual distribution.
