---
name: research-ga-top-k
title: 'Generative Agents: Retrieving the Top Memories'
tags: [research-papers, agents, memory, simulation]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Once every memory has a score, the agent takes the top few for the current decision. Those memories are placed in the prompt, so only the most useful ones use the context window.

### From theory to code

Implement `top_k_memories(memories, k)`, returning the k best memory names.

### Constraints

- Return names, not the pairs.

### Hints

<details>
<summary>Hint 1</summary>

Sort the pairs by score descending, then take the names of the first k.

</details>

## Theory

### The simple version

A fixed-size retrieval keeps the prompt within budget while still giving the agent its most relevant context.

### The formula

$$\text{top}_k = \{\,m : \text{rank}(m) \le k\,\}$$

### How NumPy/PyTorch actually implements this

Agent memory modules return the top memories by retrieval score in exactly this way.

## Explanation

Sorting by a negated score gives descending order without a reverse flag.
