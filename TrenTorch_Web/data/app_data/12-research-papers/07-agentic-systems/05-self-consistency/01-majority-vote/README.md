---
name: research-sc-majority-vote
title: 'Self-Consistency: Majority Vote'
tags: [research-papers, agents, reasoning, sampling]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Self-consistency (Wang et al., 2022) samples several reasoning paths at a non-zero temperature, then takes the answer most paths agree on. It replaces greedy decoding with a vote over diverse reasoning.

### From theory to code

Implement `majority_vote(answers)`, returning the most frequent answer with ties broken by first appearance.

### Constraints

- Ties go to the earliest answer.

### Hints

<details>
<summary>Hint 1</summary>

Count occurrences, then return the answer with the highest count, scanning in order so ties keep the earlier one.

</details>

## Theory

### The simple version

Independent reasoning paths make correct answers agree more often than any single wrong one, so the majority is a robust estimate of the right answer.

### The formula

$$\hat a = \arg\max_a \sum_{i=1}^{N}\mathbb{1}[a_i = a]$$

### How NumPy/PyTorch actually implements this

The paper's evaluation counts answers over sampled completions and returns the mode.

## Explanation

Scanning in order is what makes the tie rule deterministic, which keeps evaluation reproducible.
