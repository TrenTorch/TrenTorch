---
name: research-lottery-remaining-fraction
title: 'The Lottery Ticket Hypothesis: Iterative Pruning'
tags: [research-papers, classical-ml, pruning, lottery-ticket]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The paper prunes iteratively: train, prune a fraction of the remaining weights, rewind, and repeat. Pruning 20 percent per round for several rounds keeps far fewer weights than one large cut, and each round compounds the last.

### From theory to code

Implement `remaining_fraction(p, rounds)`, returning `(1 - p) ** rounds`.

### Constraints

- `p` is the per-round prune fraction.

### Hints

<details>
<summary>Hint 1</summary>

Raise the per-round keep fraction to the number of rounds.

</details>

## Theory

### The simple version

Each round keeps `1 - p` of what was left, so the fractions multiply. This is why many small rounds reach very high sparsity.

### The formula

$$f_k = (1 - p)^k$$

### How NumPy/PyTorch actually implements this

Iterative pruning schedules compute the same geometric sequence for the target density at each round.

## Explanation

The geometric decay is the schedule the paper uses to reach high sparsity while still finding trainable subnetworks.
