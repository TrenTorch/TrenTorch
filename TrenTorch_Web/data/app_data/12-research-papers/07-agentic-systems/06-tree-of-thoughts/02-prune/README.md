---
name: research-tot-prune
title: 'Tree of Thoughts: Pruning Weak Branches'
tags: [research-papers, agents, search, reasoning]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Tree of Thoughts can also drop branches the model judges hopeless, instead of keeping a fixed beam. A score threshold is the simplest pruning rule.

### From theory to code

Implement `prune_below(score, threshold)`, returning whether the branch survives pruning.

### Constraints

- The comparison is inclusive.

### Hints

<details>
<summary>Hint 1</summary>

Compare the score with the threshold.

</details>

## Theory

### The simple version

Pruning spends the search budget only on branches with a reasonable chance of success. A threshold that is too high can remove the only correct path, so it must be tuned.

### The formula

$$\text{keep}(s) \iff V(s) \ge \theta$$

### How NumPy/PyTorch actually implements this

Search-based agents apply a score threshold after each expansion step.

## Explanation

The value V comes from the model's own evaluation of the partial solution, which the paper prompts for explicitly.
