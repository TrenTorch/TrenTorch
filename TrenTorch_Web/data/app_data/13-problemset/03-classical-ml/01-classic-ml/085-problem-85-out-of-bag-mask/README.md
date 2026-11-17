---
name: problem-85-out-of-bag-mask
title: 'Out-of-Bag Mask'
tags: [problemset, classical-ml-trees-ensembles, out-of-bag]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'out of bag'
hint: 'start with all True and set the drawn indices to False'
tools: [NumPy]
---

## Statement

Compute the out-of-bag mask of a bootstrap sample. `n` is the size of the original dataset and `bootstrap_indices` are the indices that were drawn (repeats allowed).

Implement `solve(n, bootstrap_indices)`.

**Returns.** Return a boolean NumPy array of length `n` that is `True` for every index that was **not** drawn.

### Examples

**Example 1**

Input:

```python
solve(10, [0, 1, 2])
```

Output:

```text
[False, False, False, True, True, True, True, True, True, True]
```

**Example 2**

Input:

```python
solve(5, [0, 2, 2])
```

Output:

```text
[False, True, False, True, True]
```

## Theory

### The simple version

Because a bootstrap sample leaves out about a third of the data, those left-out ("out-of-bag") points are a free validation set for the model trained on that sample. The mask says which points they are.

### The definition

$$\text{oob}_i=\neg\,\exists j:\;\text{idx}_j=i$$

### Why it matters

- Samples left out of a bootstrap are a free validation set for that tree.
- The mask identifies them.

### How it works

1. Start with all `True`.
2. Set each drawn index to `False`.

### Worked example

With $n=10$ and drawn indices $(0,1,2)$, those three become `False` and the other seven stay `True`: [False, False, False, True, True, True, True, True, True, True].

## Explanation

Start with everything marked out of bag and switch off every index that was drawn. Drawing an index several times has the same effect as drawing it once.
