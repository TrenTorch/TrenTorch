---
name: problem-127-average-pooling-2d
title: 'Average Pooling 2D'
tags: [problemset, dl-core, cnn-basics]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'cnn basics'
hint: 'for each window position take the mean of X[i*s:i*s+k, j*s:j*s+k]'
tools: [NumPy]
---

## Statement

Apply 2-D average pooling with a `k`×`k` window and stride `s` (default 1). Windows that do not fit entirely inside the input are not used. Pass `s=k` for the usual non-overlapping pooling.

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
[[2.5]]
```

**Example 2**

Input:

```python
solve([[1, 2, 5, 6], [3, 4, 7, 8], [9, 1, 2, 3], [4, 5, 6, 7]], 2, 2)
```

Output:

```text
[[2.5, 6.5], [4.75, 4.5]]
```

## Theory

### The simple version

Average pooling summarises each neighbourhood by its mean. Unlike max pooling it keeps information about the whole window instead of only its strongest entry, which gives smoother, less selective features. Global average pooling (one window over the whole map) is common before the final classifier.

### The formula

$$Y_{ij}=\frac1{k^2}\sum_{u,v=0}^{k-1}X_{is+u,\;js+v}$$

## Explanation

The window means are computed independently. In the first example the single window has mean $(1+3+2+4)/4=2.5$.
