---
name: research-flash-online-softmax-merge
title: 'FlashAttention: Merging Softmax Blocks'
tags: [research-papers, systems, attention, kernels]
difficulty: Advanced
---

## Statement

### The problem, from first principles

FlashAttention (Dao et al., 2022) computes exact attention one block of keys at a time, so the full score matrix never reaches slow memory. Each block contributes a running max and a running sum. Two such summaries merge exactly by rescaling to the larger max.

### From theory to code

Implement `online_softmax_merge(m1, l1, m2, l2)`, merging two blocks' softmax statistics exactly.

### Constraints

- The result must equal the softmax normalizer computed over the union.

### Hints

<details>
<summary>Hint 1</summary>

Take the larger max as the new max, then scale each sum by `exp(old_max - new_max)` before adding.

</details>

## Theory

### The simple version

This is the identity that lets the kernel stream over key blocks while keeping an exact softmax. The rescale stops overflow because every exponent is at most zero.

### The formula

$$m = \max(m_1, m_2), \qquad \ell = \ell_1 e^{m_1 - m} + \ell_2 e^{m_2 - m}$$

### How NumPy/PyTorch actually implements this

The FlashAttention CUDA kernel updates these two numbers per query row on each key tile.

## Explanation

The statistics are exactly the ones a streaming softmax tracks, so the merge matches a single pass over all scores.
