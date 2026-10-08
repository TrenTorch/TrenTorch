---
name: research-ptr-pointer-sequence
title: 'Pointer Networks: A Pointer Sequence'
tags: [research-papers, sequence-models, attention, pointer]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A pointer network decodes a whole output sequence of input positions. At each step it points at one input, and the pointed positions form the answer, such as a sorted order or a convex hull.

### From theory to code

Implement `pointer_argmax_sequence(scores_seq)`, the greedy pointed position for every step.

### Constraints

- Return Python ints.

### Hints

<details>
<summary>Hint 1</summary>

Take the argmax along the input axis for each row.

</details>

## Theory

### The simple version

Greedy pointing decodes the output one step at a time, and this sequence is the output of that process.

### The formula

$$\hat C_t = \arg\max_i\, u^{(t)}_i$$

### How NumPy/PyTorch actually implements this

Sequence decoders with copy or pointer heads record the chosen index at each step in the same way.

## Explanation

Pointing repeatedly at the same input is allowed in the basic model, which the paper handles in the task design.
