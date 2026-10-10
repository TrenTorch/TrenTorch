---
name: early-stopping-patience-company-249
title: 'early-stopping-patience — Uber case'
tags: [problemset, dl-training-theory, overfitting-and-generalization, uber]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'Probability & Statistics'
caseCompany: 'Uber'
hint: 'best and bad counters; return the index when bad >= patience, else -1'
---

## Statement

Uber-inspired model-training pipeline monitors validation loss and wants to stop once improvement has stalled for a configured patience window. You need to implement the early-stopping counter exactly so the training job stops at the intended epoch.

Scan the validation losses in order. An epoch is **bad** if its loss is not strictly lower than the best loss so far, and a new best resets the bad-epoch counter. Return the 0-based index of the first epoch at which the counter reaches `patience`, or `-1` if that never happens.

Implement `solve(losses,patience)`.

**Returns.** Return an `int`.

Scan the validation losses in order. An epoch is **bad** if its loss is not strictly lower than the best loss so far, and a new best resets the bad-epoch counter. Return the 0-based index of the first epoch at which the counter reaches `patience`, or `-1` if that never happens.

Implement `solve(losses,patience)`.

**Returns.** Return an `int`.

### Examples

**Example 1**

Input:

```python
solve([0.9, 0.8, 0.81, 0.82], 2)
```

Output:

```text
3
```

**Example 2**

Input:

```python
solve([0.9, 0.8, 0.7], 2)
```

Output:

```text
-1
```

## Theory

### The simple version

Training for too long makes a model memorise its training set. Early stopping watches the validation loss and ends training when it has failed to improve for `patience` consecutive epochs, then typically restores the best checkpoint.

### The rule

$$\text{bad}_t=\begin{cases}0&L_t<\min_{s<t}L_s\\\text{bad}_{t-1}+1&\text{otherwise}\end{cases}\qquad\text{stop at the first }t\text{ with bad}_t\ge\text{patience}$$

### Why it matters

- Training too long overfits: validation loss rises while training loss keeps falling.
- Early stopping ends training after `patience` epochs without a new best loss.

### How it works

1. Track the best loss and the number of epochs since it improved.
2. A strictly lower loss resets the counter; otherwise increase it.
3. Return the index when the counter reaches `patience`, else $-1$.

### Worked example

Losses $(0.9,0.8,0.81,0.82)$ with patience $2$: index $1$ is the best ($0.8$); index $2$ is worse (counter $1$); index $3$ is worse (counter $2$), so training stops at index 3.

## Explanation

In the first example the best loss $0.8$ occurs at index 1; indices 2 and 3 are both worse, so the counter reaches $2$ at index 3. A steadily improving loss (second example) never stops, and the function returns $-1$.
