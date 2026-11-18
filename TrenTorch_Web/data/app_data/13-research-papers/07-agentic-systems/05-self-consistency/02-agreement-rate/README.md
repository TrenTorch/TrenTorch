---
name: research-sc-agreement-rate
title: 'Self-Consistency: Agreement Rate'
tags: [research-papers, agents, reasoning, sampling]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The agreement rate measures how confident the sampled reasoning is. When most paths reach the same answer, the vote is reliable; when they scatter, the model is unsure.

### From theory to code

Implement `agreement_rate(answers)`, the share of answers that match the majority.

### Constraints

- The list is non-empty.

### Hints

<details>
<summary>Hint 1</summary>

Count the answers, take the largest count, and divide by the total.

</details>

## Theory

### The simple version

A low agreement rate flags a question the model finds hard, which is a useful signal to escalate or resample.

### The formula

$$\text{agree} = \frac{\max_a \#\{i : a_i = a\}}{N}$$

### How NumPy/PyTorch actually implements this

Self-consistency analyses report this rate to separate confident and uncertain questions.

## Explanation

The rate equals one exactly when every sampled path reaches the same answer.
