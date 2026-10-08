---
name: research-ptr-pointer-distribution
title: 'Pointer Networks: The Pointer Distribution'
tags: [research-papers, sequence-models, attention, pointer]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Pointer networks (Vinyals et al., 2015) output a position in the input rather than a word from a fixed vocabulary. The output is a softmax over the input positions, so the vocabulary can change with every input.

### From theory to code

Implement `pointer_distribution(scores)`, a stable softmax over the input positions.

### Constraints

- The output sums to one.

### Hints

<details>
<summary>Hint 1</summary>

Subtract the maximum score, exponentiate, and normalize.

</details>

## Theory

### The simple version

Since the output set is the input itself, the model can point to any token it was given, which suits sorting and combinatorial problems.

### The formula

$$p(C_i) = \operatorname{softmax}_i\big(u_i\big), \qquad u_i = v^\top\tanh(W_1 e_i + W_2 d_t)$$

### How NumPy/PyTorch actually implements this

Implementations compute the same softmax over encoder positions for each decoding step.

## Explanation

The scores come from additive attention, but the softmax is over input positions rather than a blended context.
