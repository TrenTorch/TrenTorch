---
name: research-mrkl-route-query
title: 'MRKL: Routing a Query to an Expert'
tags: [research-papers, agents, tool-use, modular]
difficulty: Beginner
---

## Statement

### The problem, from first principles

MRKL (Karpas et al., 2022) routes a language model's request to specialized modules, such as a calculator or a knowledge base. The router is the first step: decide which module should handle the query.

### From theory to code

Implement `route_query(query, experts)`, returning the expert whose keyword appears in the query.

### Constraints

- Matching is case-insensitive; the first expert in the list wins.

### Hints

<details>
<summary>Hint 1</summary>

Lowercase the query, then scan the keyword list in order for the first keyword contained in it.

</details>

## Theory

### The simple version

A keyword router is transparent and cheap. The paper's point is that the language model can handle language while the experts handle exact computation.

### The formula

$$e^* = \text{expert}\big(\min\{i : k_i \subseteq q\}\big)$$

### How NumPy/PyTorch actually implements this

Modular agent frameworks use exactly such routing tables before invoking a specific tool.

## Explanation

Ordering the experts gives a deterministic priority when two keywords both match.
