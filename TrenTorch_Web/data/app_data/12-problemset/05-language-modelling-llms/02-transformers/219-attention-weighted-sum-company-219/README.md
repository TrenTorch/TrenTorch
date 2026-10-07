---
name: attention-weighted-sum-company-219
title: 'attention-weighted-sum — Swiggy case'
tags: [problemset, sequence-models-attention, attention-mechanism, swiggy]
difficulty: Beginner
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'Transformers'
caseCompany: 'Swiggy'
hint: 'softmax(scores) @ V'
tools: [NumPy]
---

## Statement

Swiggy-inspired recommendation model combines several encoded signals using learned attention weights. You need to turn the raw attention scores into weights with a softmax and compute the weighted sum of the value vectors, so the model produces the intended context representation.

`scores` are the raw (unnormalised) attention scores for one query over $n$ items and `V` is the $n\times d$ matrix of their value vectors. Turn the scores into weights with a stable softmax and return the weighted sum of the rows of `V`.

Implement `solve(scores,V)`.

**Returns.** Return a float NumPy vector of length $d$.

### Examples

**Example 1**

Input:

```python
solve([0.0, 0.0], [[1.0, 2.0], [3.0, 4.0]])
```

Output:

```text
[2.0, 3.0]
```

**Example 2**

Input:

```python
solve([10.0, 0.0], [[1.0, 0.0], [0.0, 1.0]])
```

Output:

```text
[0.999955, 4.5e-05]
```

## Theory

### The simple version

Attention lets a model decide how much to read from each of several inputs. Scores rate each input, a softmax turns them into non-negative weights that add up to 1, and the output is the blend of the inputs using those weights: a context vector dominated by the highest-scored items.

### The formula

$$w=\operatorname{softmax}(s),\qquad c=\sum_iw_i\,v_i=w^\top V$$

## Explanation

Equal scores give equal weights, i.e. the plain average of the value rows (first example gives $(2,3)$). A much larger score makes the weight nearly one-hot, so the output almost copies that item (second example, about $(1,0)$). The maximum score is subtracted before exponentiating for stability.
