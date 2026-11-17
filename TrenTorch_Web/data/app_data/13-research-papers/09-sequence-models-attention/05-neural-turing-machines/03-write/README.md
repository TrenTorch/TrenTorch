---
name: research-ntm-write
title: 'Neural Turing Machines: Erase and Add Write'
tags: [research-papers, sequence-models, memory, neural-computation]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

The NTM writes by erasing part of each addressed row and then adding new content, both weighted by the write distribution. Erase and add are separate so the model can overwrite a slot cleanly.

### From theory to code

Implement `ntm_write(memory, w, erase, add)`, the erase-then-add update.

### Constraints

- `erase` values are between 0 and 1.

### Hints

<details>
<summary>Hint 1</summary>

Scale each row's old content by one minus w times erase, then add w times add.

</details>

## Theory

### The simple version

Erase-then-add is differentiable and lets the controller replace a slot's content rather than only accumulate into it.

### The formula

$$M_t(i) = M_{t-1}(i)\odot\big(1 - w_t(i)\,e_t\big) + w_t(i)\,a_t$$

### How NumPy/PyTorch actually implements this

NTM-style write heads perform this update on the memory matrix each step.

## Explanation

The update is applied to every row; rows with zero write weight are untouched.
