---
name: research-lottery-apply-mask
title: 'The Lottery Ticket Hypothesis: Applying the Mask'
tags: [research-papers, classical-ml, pruning, lottery-ticket]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Once a mask is chosen, the sparse network is just the original weights with the pruned entries forced to zero. The paper's key step is to reset the kept weights to their initial values, which this question does not do yet.

### From theory to code

Implement `apply_mask(w, mask)`, which zeros the weights where the mask is False.

### Constraints

- `mask` is boolean and matches the shape of `w`.

### Hints

<details>
<summary>Hint 1</summary>

Multiply element-wise, letting `False` become 0.

</details>

## Theory

### The simple version

A zero weight contributes nothing to the output, so masking is equivalent to removing the connection. Keeping the array shape lets the masked network use the same code as the dense one.

### The formula

$$\tilde w = m \odot w$$

### How NumPy/PyTorch actually implements this

In PyTorch, `prune.custom_from_mask` and manual `weight.mul_(mask)` apply the same operation.

## Explanation

The element-wise product zeros the pruned entries and leaves the kept ones unchanged.
