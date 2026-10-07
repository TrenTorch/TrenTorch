---
name: problem-167-attention-weighted-sum
title: 'Attention Weighted Sum'
tags: [problemset, sequence-models-attention, attention-mechanism]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'attention mechanism'
hint: 'weights @ values'
tools: [NumPy]
---

## Statement

Compute the output of the last step of attention: the weighted sum of the value vectors using precomputed attention weights. `weights` has shape `(n_queries, n_keys)` and `values` has shape `(n_keys, d_v)`.

Implement `solve(weights, values)`.

**Returns.** Return a NumPy array of shape `(n_queries, d_v)`: row $i$ is $\sum_j w_{ij}v_j$.

### Examples

**Example 1**

Input:

```python
solve([[0.5, 0.5]], [[1.0, 2.0], [3.0, 4.0]])
```

Output:

```text
[[2.0, 3.0]]
```

**Example 2**

Input:

```python
solve([[1.0, 0.0], [0.25, 0.75]], [[10.0], [20.0]])
```

Output:

```text
[[10.0], [17.5]]
```

## Theory

### The simple version

Once attention has decided _how much_ each query cares about each key (the weights, rows that sum to 1), the output is simply a blend of the value vectors with those proportions. A weight of 1 on one key copies that key's value; equal weights average them.

### The formula

$$\text{out}=W\,V,\qquad \text{out}_i=\sum_jw_{ij}\,v_j$$

## Explanation

This is one matrix product. In the first example the two values are averaged to $(2,3)$. In the second, the first query copies the first value ($10$) and the second blends $0.25\cdot10+0.75\cdot20=17.5$.
