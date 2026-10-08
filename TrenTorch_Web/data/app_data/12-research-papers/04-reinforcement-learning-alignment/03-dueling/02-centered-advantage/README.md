---
name: research-dueling-centered-advantage
title: 'Dueling Networks: Centering the Advantages'
tags: [research-papers, reinforcement-learning, deep-q-learning, architectures]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Before combining with V, the advantages are centered so they have zero mean across actions. This is the piece that pins down the value and advantage streams.

### From theory to code

Implement `centered_advantage(A)`, subtracting the mean of the advantage vector.

### Constraints

- The output sums to zero.

### Hints

<details>
<summary>Hint 1</summary>

Subtract `A.mean()` from every entry.

</details>

## Theory

### The simple version

Centering removes the part of the advantage that every action shares, which belongs to the value stream. What remains is purely about relative action quality.

### The formula

$$\tilde A(a) = A(a) - \bar A, \qquad \bar A = \frac{1}{|\mathcal{A}|}\sum_{a'} A(a')$$

### How NumPy/PyTorch actually implements this

The same centering appears as a baseline subtraction in policy-gradient methods.

## Explanation

The result has zero mean by construction, which is the constraint the aggregation relies on.
