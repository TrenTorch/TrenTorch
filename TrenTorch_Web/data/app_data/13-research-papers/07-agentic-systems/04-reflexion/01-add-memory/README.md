---
name: research-reflexion-add-memory
title: 'Reflexion: Keeping a Bounded Memory'
tags: [research-papers, agents, memory, self-improvement]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Reflexion (Shinn et al., 2023) stores verbal reflections about past failures and feeds them into the next attempt. The memory has to stay bounded, so only the most recent reflections are kept.

### From theory to code

Implement `add_reflection(memory, reflection, max_items)`, returning the bounded memory with the new reflection added.

### Constraints

- A zero capacity keeps an empty memory.

### Hints

<details>
<summary>Hint 1</summary>

Build a new list with the reflection at the end, then slice off the oldest entries.

</details>

## Theory

### The simple version

A bounded window keeps the prompt short while still carrying the most relevant recent lessons. Returning a new list keeps the caller's memory unchanged.

### The formula

$$M \leftarrow \text{last}_{k}\big(M \,\|\, [r]\big)$$

### How NumPy/PyTorch actually implements this

Agent memory stores in the Reflexion code keep a list of reflections with the same truncation.

## Explanation

The slice keeps the newest k entries, which is a first-in, first-out memory.
