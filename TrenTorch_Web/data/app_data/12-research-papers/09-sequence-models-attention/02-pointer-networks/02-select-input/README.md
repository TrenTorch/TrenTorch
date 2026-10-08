---
name: research-ptr-select-input
title: 'Pointer Networks: Selecting the Pointed Input'
tags: [research-papers, sequence-models, attention, pointer]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The output of a pointer network is the input element at the chosen position. Selecting it is the argmax over the pointer distribution followed by a lookup.

### From theory to code

Implement `select_input(scores, inputs)`, returning the input at the highest-scoring position.

### Constraints

- Ties go to the first position.

### Hints

<details>
<summary>Hint 1</summary>

Take the argmax of the scores and index the input list.

</details>

## Theory

### The simple version

Copying the chosen input rather than generating a word is what gives pointer networks their exact, vocabulary-free output.

### The formula

$$\hat y_t = x_{\arg\max_i p(C_i)}$$

### How NumPy/PyTorch actually implements this

Copy-mechanism models use the same selection to emit tokens that appear in the source.

## Explanation

The argmax is the greedy decoding choice; beam search can keep several pointer choices instead.
