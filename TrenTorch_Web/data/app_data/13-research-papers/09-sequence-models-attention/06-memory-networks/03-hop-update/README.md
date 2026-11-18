---
name: research-memnet-hop
title: 'Memory Networks: The Multi-hop Update'
tags: [research-papers, sequence-models, memory, question-answering]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Memory Networks reason over several hops: each hop reads memory with the current state, then updates the state with the read result. Later hops can follow chains of facts.

### From theory to code

Implement `hop_update(u, o)`, the state update between hops.

### Constraints

- The update is a simple sum.

### Hints

<details>
<summary>Hint 1</summary>

Add the memory output to the current state.

</details>

## Theory

### The simple version

Stacking hops lets the model chain facts: the first read finds an entity, and the next finds what is known about it.

### The formula

$$u^{(k+1)} = u^{(k)} + o^{(k)}$$

### How NumPy/PyTorch actually implements this

Multi-hop memory networks run this update between a fixed number of read steps.

## Explanation

The paper uses this residual-style update with a learned hop-specific embedding in later variants.
