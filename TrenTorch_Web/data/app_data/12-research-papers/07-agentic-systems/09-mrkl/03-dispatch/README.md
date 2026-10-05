---
name: research-mrkl-dispatch
title: 'MRKL: Dispatching to Experts'
tags: [research-papers, agents, tool-use, modular]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

MRKL systems dispatch a query to a module and return the module's output. A router with a fallback to the language model covers every query, whether or not an expert applies.

### From theory to code

Implement `dispatch(query, routes, fallback)`, running the first matching route or the fallback.

### Constraints

- Routes are checked in order.

### Hints

<details>
<summary>Hint 1</summary>

Find the first route whose keyword matches the lowercased query and call it with the original query; otherwise call the fallback.

</details>

## Theory

### The simple version

Experts handle the cases they are built for, and the language model handles everything else. The fallback makes the system total.

### The formula

$$\text{out} = \begin{cases} f_i(q) & i = \min\{i : k_i \subseteq q\} \\ \text{fallback}(q) & \text{otherwise} \end{cases}$$

### How NumPy/PyTorch actually implements this

MRKL-style agents call this dispatch once per user turn before returning the result.

## Explanation

The dispatch is a routing table with a default, the same shape as a switch statement with a catch-all.
