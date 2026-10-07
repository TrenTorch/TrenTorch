---
name: masked-sequence-mean-company-218
title: 'masked-sequence-mean — Flipkart case'
tags: [problemset, sequence-models-attention, sequence-padding-and-masking, flipkart]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'Probability & Statistics'
caseCompany: 'Flipkart'
hint: 'X[mask].mean(axis=0), zeros if the mask is empty'
tools: [NumPy]
---

## Statement

Flipkart-inspired sequence model receives padded item histories where padding positions must not influence the representation. You need to compute the mean over only the unmasked positions so downstream ranking features are not biased by padding.

`X` holds one embedding per row of a padded sequence and `mask[i]` is `1` (or `True`) for real positions and `0` for padding. Return the average of the real embeddings only. If no position is real, return the zero vector.

Implement `solve(X,mask)`.

**Returns.** Return a float NumPy vector of length `X.shape[1]`.

### Examples

**Example 1**

Input:

```python
solve([[1, 2], [3, 4], [9, 9]], [1, 1, 0])
```

Output:

```text
[2.0, 3.0]
```

**Example 2**

Input:

```python
solve([[5.0, 5.0]], [0])
```

Output:

```text
[0.0, 0.0]
```

## Theory

### The simple version

Histories of different lengths are padded to a common length. If padding rows were included in a plain average, the result would depend on how much padding a sequence happened to receive. Masking them out makes the representation depend only on the real items.

### The formula

$$\bar e=\frac{\sum_im_i\,e_i}{\sum_im_i}$$

## Explanation

In the first example the padding row $(9,9)$ is ignored and the result is the mean of $(1,2)$ and $(3,4)$, i.e. $(2,3)$. With no valid row the mean is undefined, so zeros are returned instead of `NaN`.
