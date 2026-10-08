---
name: research-spec-residual
title: 'Speculative Decoding: The Residual Distribution'
tags: [research-papers, systems, inference, decoding]
difficulty: Advanced
---

## Statement

### The problem, from first principles

When a drafted token is rejected, the replacement is sampled from the residual distribution, the part of the target that the draft under-covered. Together with the acceptance rule this keeps the output exactly target-distributed.

### From theory to code

Implement `residual_distribution(p, q)`, the positive part of the difference, renormalized.

### Constraints

- The result sums to one when any residual mass exists.

### Hints

<details>
<summary>Hint 1</summary>

Take the element-wise maximum of p minus q and zero, then divide by its sum.

</details>

## Theory

### The simple version

The residual is exactly where the target puts more probability than the draft, so resampling there completes the distribution correctly after a rejection.

### The formula

$$p_{\text{res}}(x) = \frac{\max(p(x) - q(x), 0)}{\sum_{x'}\max(p(x') - q(x'), 0)}$$

### How NumPy/PyTorch actually implements this

Speculative decoding implementations sample the replacement token from this renormalized distribution.

## Explanation

The normalizer is one minus the total acceptance probability, which is positive whenever a rejection can happen.
