---
name: problem-143-early-stopping
title: 'Early Stopping'
tags: [problemset, dl-training-theory, regularization]
difficulty: Advanced
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'regularization'
hint: 'best and bad counters: reset bad on a strictly lower loss, stop when bad >= patience'
tools: [NumPy]
---

## Statement

Decide whether training should stop early. Scan the validation losses in order; an epoch is **bad** if its loss is not strictly lower than the best loss seen so far, and the bad-epoch counter resets whenever a new best is reached. Return `True` as soon as the counter reaches `patience`.

Implement `solve(losses,patience)`.

**Returns.** Return `True` if training would have stopped somewhere in the list, otherwise `False`.

### Examples

**Example 1**

Input:

```python
solve([1.0, 0.9, 0.95, 0.96], 1)
```

Output:

```text
True
```

**Example 2**

Input:

```python
solve([1.0, 0.9, 0.95, 0.96], 3)
```

Output:

```text
False
```

**Example 3**

Input:

```python
solve([1.0, 0.9, 0.8, 0.7], 2)
```

Output:

```text
False
```

## Theory

### The simple version

Training too long makes a model memorise the training set, and its validation loss starts rising even as the training loss keeps falling. Early stopping watches the validation loss and stops once it has failed to improve for a number of epochs (the _patience_), usually keeping the best checkpoint.

### The rule

Track $\text{best}=\min$ so far and $\text{bad}$ = consecutive epochs without a new best. Stop when $\text{bad}\ge\text{patience}$.

## Explanation

In the first example the loss improves to $0.9$ and then gets worse once, which already exhausts a patience of $1$. With a patience of $3$ (second example) only two bad epochs occur, so training would continue. A steadily falling loss never stops (third example).
