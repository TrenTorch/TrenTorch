---
name: problem-124-convolution-output-shape
title: 'Convolution Output Shape'
tags: [problemset, dl-core, cnn-basics]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'cnn basics'
hint: '(W + 2*P - K) // S + 1'
tools: [NumPy]
---

## Statement

Compute the output size of a convolution along one dimension from the input size `W`, kernel size `K`, padding `P` (added on both sides) and stride `S`: $\lfloor (W+2P-K)/S\rfloor+1$.

Implement `solve(W,K,P,S)`.

**Returns.** Return an integer. A kernel larger than the padded input gives a value of 0 or less, meaning no valid position.

### Examples

**Example 1**

Input:

```python
solve(5, 3, 0, 1)
```

Output:

```text
3
```

**Example 2**

Input:

```python
solve(7, 3, 1, 2)
```

Output:

```text
4
```

## Theory

### The simple version

A convolution slides a window across the input. The output size is the number of positions the window can take: after padding, the window of width $K$ starts at $0,S,2S,\dots$ as long as it still fits.

### The formula

$$W_{out}=\left\lfloor\frac{W+2P-K}{S}\right\rfloor+1$$

## Explanation

For the first example, $W=5$, $K=3$, no padding, stride 1 gives $5-3+1=3$ positions. With padding $1$ and stride $2$ on a width-7 input, $\lfloor(7+2-3)/2\rfloor+1=4$. "Same" padding for an odd kernel is $P=(K-1)/2$.
