---
name: gini-impurity-company-208
title: 'gini-impurity — Cloudflare case'
tags: [problemset, classical-ml-trees-ensembles, decision-trees, cloudflare]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Classification'
topic: 'Classification'
caseCompany: 'Cloudflare'
hint: 'p = mean(y == 1); 1 - p^2 - (1-p)^2'
tools: [NumPy]
---

## Statement

This is a hypothetical engineering scenario inspired by the kind of work a **Cloudflare** ranking and experimentation team might handle; it is not a real interview question or a claim that Cloudflare uses this exact task. The team needs a reliable implementation for decision-tree training in a production-oriented ML workflow. A small implementation error can change the model input or metric enough to make a downstream result misleading.

Compute the Gini impurity of a binary label vector for a decision-tree node.

Compute $1-p^2-(1-p)^2$ where $p$ is the fraction of labels equal to `1`. Labels must be `0` or `1`; an empty node has impurity `0.0`.

Implement `solve(y)`.

**Returns.** Return a float between $0$ and $0.5$.

Compute $1-p^2-(1-p)^2$ where $p$ is the fraction of labels equal to `1`. Labels must be `0` or `1`; an empty node has impurity `0.0`.

Implement `solve(y)`.

**Returns.** Return a float between $0$ and $0.5$.

### Examples

**Example 1**

Input:

```python
solve([0, 0, 1, 1])
```

Output:

```text
0.5
```

**Example 2**

Input:

```python
solve([1, 1, 1, 1])
```

Output:

```text
0.0
```

**Example 3**

Input:

```python
solve([0, 1, 1, 1])
```

Output:

```text
0.375
```

## Theory

### The simple version

Gini impurity is the probability that two items drawn at random from the node (with replacement) have different labels. A pure node scores $0$; a perfectly mixed binary node scores $0.5$. A decision tree prefers splits that produce purer children.

### The formula

$$G=1-p^2-(1-p)^2=2p(1-p)$$

### Why it matters

- Decision trees choose splits that make the child nodes purer, and Gini impurity measures how mixed a node is.
- It is the chance that two random items from the node have different labels.

### How it works

1. Compute $p$, the fraction of labels equal to $1$.
2. Return $1-p^2-(1-p)^2$.

### Worked example

Labels $(0,0,1,1)$ give $p=0.5$, so the impurity is $1-0.25-0.25=0.5$, the maximum for two classes.

## Explanation

For a $75\%/25\%$ node (third example) $G=2\cdot0.75\cdot0.25=0.375$. The expression is symmetric in the two classes and peaks at $p=0.5$.
