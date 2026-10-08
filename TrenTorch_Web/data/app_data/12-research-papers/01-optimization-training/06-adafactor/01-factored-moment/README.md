---
name: research-adafactor-factored-moment
title: 'Adafactor: The Factored Second Moment'
tags: [research-papers, optimization, memory]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Adafactor (Shazeer & Stern, 2018) stores the second moment of a weight matrix as a row vector and a column vector instead of a full matrix. The full estimate is rebuilt as an outer product, which costs sublinear memory.

### From theory to code

Implement `factored_second_moment(row, col)`, the rank-one reconstruction of the second moment.

### Constraints

- Normalize by the total of the row sums.

### Hints

<details>
<summary>Hint 1</summary>

Take the outer product of the row and column vectors and divide by the sum of the row sums.

</details>

## Theory

### The simple version

Storing n plus m numbers instead of n times m is the memory saving. The rank-one reconstruction is exact when the true second moment has rank one.

### The formula

$$\hat V_{ij} = \frac{R_i C_j}{\sum_k R_k}$$

### How NumPy/PyTorch actually implements this

Adafactor's implementation keeps only these two vectors per matrix parameter.

## Explanation

Hand case: row sums are [1, 2], total 3, so V[0,0] = 1*3/3 = 1 and V[1,1] = 2*4/3.
