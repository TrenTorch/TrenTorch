---
name: problem-126-max-pooling-2d
title: 'Max Pooling 2D'
tags: [problemset, dl-core, cnn-basics]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'cnn basics'
hint: 'for each window position take the max of X[i*s:i*s+k, j*s:j*s+k]'
tools: [NumPy]
---

## Statement

Apply 2-D max pooling with a `k`×`k` window and stride `s` (default 1). Windows that do not fit entirely inside the input are not used. Pass `s=k` for the usual non-overlapping pooling.

Implement `solve(X,k,s=1)`.

**Returns.** Return a float array of shape `((H - k)//s + 1, (W - k)//s + 1)`; if the window is larger than the input the result is empty.

### Examples

**Example 1**

Input:

```python
solve([[1, 3], [2, 4]], 2)
```

Output:

```text
[[4.0]]
```

**Example 2**

Input:

```python
solve([[1, 2, 5, 6], [3, 4, 7, 8], [9, 1, 2, 3], [4, 5, 6, 7]], 2, 2)
```

Output:

```text
[[4.0, 8.0], [9.0, 7.0]]
```

## Theory

### The simple version

Pooling shrinks a feature map by summarising each small neighbourhood with one number. Max pooling keeps the strongest response, so a feature detected anywhere inside the window survives, which gives the network some tolerance to small shifts.

### The formula

$$Y_{ij}=\max_{0\le u,v<k}X_{is+u,\;js+v}$$

## Explanation

With `s=k` the windows tile the input without overlap (second example: four $2\times2$ blocks give `[[4, 8], [9, 7]]`). The default stride of $1$ produces overlapping windows. Pooling has no learnable parameters.
