---
name: roc-best-threshold-company-229
title: 'roc-best-threshold — Reddit case'
tags: [problemset, classical-ml, metrics-and-evaluation, reddit]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classification'
topic: 'Classification'
caseCompany: 'Reddit'
hint: 'for each unique score t: J = TPR - FPR with score >= t; keep the max (smallest t on ties)'
tools: [NumPy]
---

## Statement

Reddit-inspired moderation model produces continuous risk scores while the operations team needs a binary decision threshold. You need to evaluate candidate thresholds and select the one that maximizes Youden’s J statistic.

Choose the decision threshold that maximises Youden's $J=\text{TPR}-\text{FPR}$. Candidate thresholds are the distinct scores; an example is predicted positive when `score >= threshold`. Labels `y` are 0/1, and if several thresholds give the same $J$ the smallest one is returned.

Implement `solve(y,scores)`.

**Returns.** Return the chosen threshold (one of the scores) as a float. A rate whose denominator is zero (no positives or no negatives) counts as 0.

Choose the decision threshold that maximises Youden's $J=\text{TPR}-\text{FPR}$. Candidate thresholds are the distinct scores; an example is predicted positive when `score >= threshold`. Labels `y` are 0/1, and if several thresholds give the same $J$ the smallest one is returned.

Implement `solve(y, scores)`.

**Returns.** Return the chosen threshold (one of the scores) as a float. A rate whose denominator is zero (no positives or no negatives) counts as 0.

### Examples

**Example 1**

Input:

```python
solve([1, 1, 0, 0], [0.9, 0.7, 0.6, 0.2])
```

Output:

```text
0.7
```

**Example 2**

Input:

```python
solve([0, 0, 1, 1], [0.1, 0.4, 0.35, 0.8])
```

Output:

```text
0.35
```

## Theory

### The simple version

A classifier outputs scores but production needs a yes/no decision. Youden's $J$ picks the threshold that best balances catching positives and avoiding false alarms: the point on the ROC curve farthest above the diagonal.

### The formula

$$J(t)=\underbrace{\frac{TP(t)}{P}}_{\text{TPR}}-\underbrace{\frac{FP(t)}{N}}_{\text{FPR}},\qquad t^*=\arg\max_tJ(t)$$

### Why it matters

- A classifier produces scores, but production needs a yes/no threshold.
- Youden's $J=\text{TPR}-\text{FPR}$ finds the point on the ROC curve that best separates the classes.

### How it works

1. Take each distinct score as a threshold.
2. Predict positive when the score is at least the threshold.
3. Compute TPR minus FPR and keep the best (smallest threshold on ties).

### Worked example

Labels $(1,1,0,0)$ with scores $(0.9,0.7,0.6,0.2)$. Threshold $0.9$: TPR $0.5$, FPR $0$, $J=0.5$. Threshold $0.7$: TPR $1$, FPR $0$, $J=1$. Threshold $0.6$: FPR $0.5$, $J=0.5$. The best is 0.7.

## Explanation

In the first example, threshold $0.7$ catches both positives and lets in no negatives, so $J=1$; the lower thresholds only add false positives. Ties are broken toward the smaller threshold because the comparison key is $(J,-t)$.
