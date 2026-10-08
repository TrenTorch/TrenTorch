---
name: problem-105-apriori-candidate-join
title: 'Apriori Candidate Join'
tags: [problemset, unsupervised-ml, association-rules]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'association rules'
hint: 'sort the itemsets; join pairs with equal prefix prev[:-1]; deduplicate'
tools: [NumPy]
---

## Statement

Perform the candidate-generation join step of the Apriori algorithm. `prev` is a collection of frequent $(k-1)$-itemsets (each a sequence of items). Sort the itemsets and join every pair whose first $k-2$ items agree, appending the last item of the second to the first. No pruning is applied.

Implement `solve(prev)`.

**Returns.** Return a sorted list of distinct $k$-item tuples.

### Examples

**Example 1**

Input:

```python
solve([('a', 'b'), ('a', 'c'), ('b', 'c')])
```

Output:

```text
[('a', 'b', 'c')]
```

**Example 2**

Input:

```python
solve([('a',), ('b',), ('c',)])
```

Output:

```text
[('a', 'b'), ('a', 'c'), ('b', 'c')]
```

## Theory

### The simple version

Apriori finds itemsets that often occur together, growing them one item at a time. To build candidates of size $k$ it combines frequent itemsets of size $k-1$. Joining only itemsets that agree on everything except the last item makes each candidate appear exactly once.

### The rule

$$\{i_1,\dots,i_{k-2},x\}\ \bowtie\ \{i_1,\dots,i_{k-2},y\}\ \longrightarrow\ \{i_1,\dots,i_{k-2},x,y\},\quad x<y$$

### Why it matters

- Apriori finds frequent itemsets by growing them one item at a time.
- Joining only sets that share a prefix generates each candidate exactly once.

### How it works

1. Sort the frequent $(k-1)$-itemsets.
2. Join pairs that agree on all but the last item.
3. Append the second one's last item.

### Worked example

Of $(a,b)$, $(a,c)$, $(b,c)$ only the first two share the prefix $(a)$. Joining gives $(a,b,c)$: [('a', 'b', 'c')].

## Explanation

Items inside each set are kept in sorted order, so a shared prefix is easy to detect. In the first example `('a','b')` and `('a','c')` share the prefix `('a',)` and produce `('a','b','c')`. The classic pruning step (discard candidates with an infrequent subset) is a separate stage that would follow.
