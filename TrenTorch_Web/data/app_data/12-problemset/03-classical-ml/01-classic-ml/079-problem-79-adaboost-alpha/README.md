---
name: problem-79-adaboost-alpha
title: 'AdaBoost Alpha'
tags: [problemset, classical-ml-trees-ensembles, boosting]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'boosting'
hint: '0.5 * ln((1 - error) / error)'
tools: [NumPy]
---

## Statement

Compute the weight $\alpha$ AdaBoost gives a weak learner from its weighted error rate $\varepsilon$.

Implement `solve(error)`.

**Returns.** Return a float. The error must lie strictly between 0 and 1 (otherwise `ValueError`). $\varepsilon<0.5$ gives a positive weight, $\varepsilon=0.5$ gives $0$, and $\varepsilon>0.5$ gives a negative weight.

### Examples

**Example 1**

Input:

```python
solve(0.2)
```

Output:

```text
0.693147
```

**Example 2**

Input:

```python
solve(0.5)
```

Output:

```text
0.0
```

**Example 3**

Input:

```python
solve(0.0)
```

Output: Raises `ValueError`.

## Theory

### The simple version

In the final AdaBoost vote, each weak learner gets a say proportional to how good it is. A learner with low error gets a big positive weight, one at chance gets none, and one that is systematically wrong gets a negative weight, which effectively flips its vote.

### The formula

$$\alpha=\frac12\ln\frac{1-\varepsilon}{\varepsilon}$$

## Explanation

The log-odds of being right grows without bound as $\varepsilon\to0$, which is why a perfectly accurate learner (error $0$) is rejected here instead of producing infinity.
