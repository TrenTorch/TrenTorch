---
name: agentic-memory-retrieval-score
title: Memory Retrieval Scoring
tags: [agentic-systems, memory, retrieval, generative-agents]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A long-lived agent accumulates thousands of memories, far too many to show the model. The influential _Generative Agents_ work retrieves them with a score built from three signals. **Recency**: recently used memories are more likely to matter, modelled by exponential decay with time since last access. **Importance**: the agent rates how significant an event was (breakfast is a 1, a breakup is a 9), so that rare but vital memories survive. **Relevance**: the cosine similarity between the memory's embedding and the current query. A weighted sum of the three ranks the memories, and the top few go into the prompt.

### From theory to code

Implement `memory_scores` and `top_memories`.

### Constraints

- Each memory is a dict with `embedding` (list of floats), `importance` (a number from 1 to 10) and `last_access` (a time in hours). `query` is an embedding list, `now` the current time in hours.
- `recency = decay ** (now - last_access)`, `importance_score = importance / 10`, `relevance = cosine(query, embedding)` (`0.0` if either vector has zero length). `memory_scores(memories, query, now, decay, weights)` returns the list of `w_r * recency + w_i * importance_score + w_s * relevance`, where `weights = (w_r, w_i, w_s)`.
- `top_memories(memories, query, now, k, decay, weights)` returns the indices of the `k` highest-scoring memories, best first, ties broken by lower index.

### Hints

<details>
<summary>Hint 1</summary>

Write a small cosine helper using `math.sqrt`.

</details>

<details>
<summary>Hint 2</summary>

Decay below 1 makes older memories score lower: with `decay = 0.99` per hour a day-old memory keeps about 79%.

</details>

## Theory

### The simple version

When recalling something, you weigh how recently you thought about it, how much it mattered and how much it relates to what you are doing right now.

### The formula

$$
s_i = w_r\,\gamma^{\,t - t_i} + w_i\,\frac{I_i}{10} + w_s\,\frac{q \cdot e_i}{\lVert q\rVert\,\lVert e_i\rVert}
$$

### How this is done in practice

The generative agents paper normalizes each component to `[0, 1]` and uses equal weights. Modern agent memory systems (MemGPT, Mem0, LangMem) keep the same ingredients and add summarization, reflection and consolidation of memories.

## Explanation

The three signals are computed independently and combined linearly, which makes it easy to see each one's effect. The tests set up scenarios in which one signal dominates.
