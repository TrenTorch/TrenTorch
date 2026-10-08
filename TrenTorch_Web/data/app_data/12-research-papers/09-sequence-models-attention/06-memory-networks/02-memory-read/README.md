---
name: research-memnet-read
title: 'Memory Networks: Reading the Output Memory'
tags: [research-papers, sequence-models, memory, question-answering]
difficulty: Beginner
---

## Statement

### The problem, from first principles

After attention chooses which memories matter, the model reads an output representation of each memory, weighted by that attention. The sum is the evidence the answer is built from.

### From theory to code

Implement `memory_output(p, outputs)`, the attention-weighted sum of output embeddings.

### Constraints

- Weights sum to one.

### Hints

<details>
<summary>Hint 1</summary>

Multiply the attention vector by the output matrix.

</details>

## Theory

### The simple version

Separate input and output embeddings let the model match questions on one representation and read answers from another.

### The formula

$$o = \sum_i p_i\,c_i$$

### How NumPy/PyTorch actually implements this

Memory network implementations compute this read once per hop.

## Explanation

The read is a convex combination of output vectors, the same form as the attention context elsewhere.
