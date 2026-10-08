---
name: research-ga-recency-score
title: 'Generative Agents: Recency Score'
tags: [research-papers, agents, memory, simulation]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Generative Agents (Park et al., 2023) retrieve memories by a mix of recency, importance and relevance. Recency decays exponentially with time since the memory was last used, so recent experiences come back first.

### From theory to code

Implement `recency_score(hours, decay)`, returning `decay ** hours`.

### Constraints

- The default decay is 0.995 per hour.

### Hints

<details>
<summary>Hint 1</summary>

Raise the decay factor to the power of the elapsed hours.

</details>

## Theory

### The simple version

Exponential decay means every hour loses the same fraction of recency, so a memory from yesterday is much weaker than one from an hour ago.

### The formula

$$r = \gamma^{\Delta t}, \qquad \gamma = 0.995$$

### How NumPy/PyTorch actually implements this

Memory retrieval modules compute this score from the timestamp of each stored memory.

## Explanation

The paper's decay of 0.995 per hour halves a memory's recency in roughly 140 hours.
