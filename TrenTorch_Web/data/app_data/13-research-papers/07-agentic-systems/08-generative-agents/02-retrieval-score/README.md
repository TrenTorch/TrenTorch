---
name: research-ga-retrieval-score
title: 'Generative Agents: Combined Retrieval Score'
tags: [research-papers, agents, memory, simulation]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A generative agent scores each memory by combining recency, importance and relevance to the current situation. Equal weights are the simplest choice, and they are what the paper uses after normalizing each term.

### From theory to code

Implement `retrieval_score(recency, importance, relevance)`, the equally weighted average.

### Constraints

- Inputs are normalized to [0, 1].

### Hints

<details>
<summary>Hint 1</summary>

Add the three values and divide by three.

</details>

## Theory

### The simple version

Each signal alone misses something: recency forgets important old events, importance ignores context, and relevance ignores how fresh a memory is. The average combines them.

### The formula

$$s = \frac{1}{3}\big(r + i + \rho\big)$$

### How NumPy/PyTorch actually implements this

The memory retrieval function sorts stored memories by this combined score.

## Explanation

With unit weights, no single factor can dominate unless the others are near zero.
