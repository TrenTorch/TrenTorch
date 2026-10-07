---
name: problem-106-support-counting
title: 'Support Counting'
tags: [problemset, unsupervised-ml, association-rules]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Classification'
topic: 'association rules'
hint: 'count transactions that contain all items, divide by the number of transactions'
tools: [NumPy]
---

## Statement

Compute the support of an itemset: the fraction of transactions that contain every item of the itemset. Items inside a transaction are treated as a set.

Implement `solve(transactions,itemset)`.

**Returns.** Return a float in $[0,1]$. The empty itemset is contained in every transaction, so its support is `1.0`. There must be at least one transaction.

### Examples

**Example 1**

Input:

```python
solve([['a', 'b'], ['a', 'c'], ['a', 'b']], ['a', 'b'])
```

Output:

```text
0.666667
```

**Example 2**

Input:

```python
solve([['a', 'b'], ['a', 'c'], ['a', 'b']], ['c'])
```

Output:

```text
0.333333
```

## Theory

### The simple version

Support says how common an itemset is: of all the shopping baskets, in what share do these items appear together? Frequent-itemset mining keeps only itemsets whose support clears a threshold.

### The formula

$$\text{support}(I)=\frac{\#\{t\in T: I\subseteq t\}}{|T|}$$

## Explanation

Each transaction is converted to a set so repeated items do not matter, and `issubset` tests containment. In the first example `{a, b}` appears in two of three baskets, giving $2/3$.
