---
name: research-distill-soft-target-ce
title: 'Distilling the Knowledge: The Soft-Target Loss'
tags: [research-papers, classical-ml, distillation, knowledge]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

The student is trained to match the teacher's softened probabilities. Cross-entropy against those soft targets carries the teacher's view of which wrong classes are close, which the hard label cannot show.

### From theory to code

Implement `soft_target_ce(teacher_logits, student_logits, T)`, computing `-sum(p_teacher * log q_student) * T**2`.

### Constraints

- Both distributions use temperature `T`.

### Hints

<details>
<summary>Hint 1</summary>

Build both softened distributions with a stable softmax, take the log of the student's, then sum the products and multiply by `T**2`.

</details>

## Theory

### The simple version

The `T**2` factor keeps gradient magnitudes comparable across temperatures, because softened targets shrink gradients by about `1 / T**2`.

### The formula

$$\mathcal{L}_{\text{soft}} = -T^2 \sum_i p_i^{(T)} \log q_i^{(T)}$$

### How NumPy/PyTorch actually implements this

Distillation frameworks implement this as `KLDivLoss` or soft cross-entropy with a `T**2` multiplier.

## Explanation

Here `p` is the teacher's softened distribution and `q` the student's; both use the same `T`.
