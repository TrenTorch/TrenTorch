---
name: problem-83-xgboost-split-gain
title: 'XGBoost Split Gain'
tags: [problemset, classical-ml-trees-ensembles, regularized-boosting]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'regularized boosting'
hint: '0.5 * (score(L) + score(R) - score(P)) with score = G^2/(H+lam)'
tools: [NumPy]
---

## Statement

Compute the XGBoost split gain from the gradient and Hessian sums of the left child (`GL`, `HL`), the right child (`GR`, `HR`) and the parent (`GP`, `HP`), with regularisation `lam`: $\tfrac12\big[\tfrac{G_L^2}{H_L+\lambda}+\tfrac{G_R^2}{H_R+\lambda}-\tfrac{G_P^2}{H_P+\lambda}\big]$. There is no extra per-leaf penalty.

Implement `solve(GL,HL,GR,HR,GP,HP,lam)`.

**Returns.** Return the gain as a float. The three sums are used as given, so the parent sums are not forced to equal the sum of the children, and the gain can be negative.

### Examples

**Example 1**

Input:

```python
solve(-2.0, 2.0, 1.0, 1.0, -1.0, 3.0, 1.0)
```

Output:

```text
0.791667
```

**Example 2**

Input:

```python
solve(3.0, 2.0, -3.0, 2.0, 0.0, 4.0, 0.0)
```

Output:

```text
4.5
```

## Theory

### The simple version

A split is worth making if the two children together fit the gradients better than the parent does. Each node has a "score" $G^2/(H+\lambda)$ measuring how much loss reduction its best leaf weight would achieve, and the gain is the improvement from splitting.

### The formula

$$\text{Gain}=\frac12\left[\frac{G_L^2}{H_L+\lambda}+\frac{G_R^2}{H_R+\lambda}-\frac{G_P^2}{H_P+\lambda}\right]$$

### Why it matters

- Trees choose the split with the highest gain, so this number decides the structure of the model.
- A non-positive gain says the split does not pay for itself.

### How it works

1. Score each node: $G^2/(H+\lambda)$.
2. Gain $=\tfrac12(\text{left}+\text{right}-\text{parent})$.

### Worked example

Left: $(-2)^2/(2+1)=1.333$; right: $1^2/(1+1)=0.5$; parent: $(-1)^2/(3+1)=0.25$. Gain $=\tfrac12(1.333+0.5-0.25)=0.791667$.

## Explanation

When $\lambda=0$ and $G_P=G_L+G_R$, $H_P=H_L+H_R$ the gain is never negative (a split cannot make the fit worse). With $\lambda>0$ the parent is regularised once instead of twice, so small splits can show a negative gain, which is a built-in pre-pruning signal.
