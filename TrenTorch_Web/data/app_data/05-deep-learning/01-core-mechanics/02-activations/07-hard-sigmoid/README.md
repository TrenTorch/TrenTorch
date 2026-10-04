---
name: dl-activations-hard-sigmoid
title: Hard Sigmoid
tags: [deep-learning, activations]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Hard Sigmoid is a piecewise linear approximation of the sigmoid function. Instead of the smooth sigmoid curve, it uses a simple linear ramp bounded between 0 and 1.

The formula is:

$$\text{hard\_sigmoid}(x) = \begin{cases}
0 & \text{if } x < -2.5 \\
\frac{x + 2.5}{5} & \text{if } -2.5 \le x \le 2.5 \\
1 & \text{if } x > 2.5
\end{cases}$$

This function is much faster to compute than sigmoid and is used in some mobile and embedded applications.

### From theory to code

Implement:

```python
hard_sigmoid(x)
```

Returns the hard sigmoid output, same shape as input.

### Constraints

- x can be any shape.
- No input modification.
- Return a new array.

### Hints

<details>
<summary>Hint 1</summary>

Use np.clip to bound values, then scale.

</details>

<details>
<summary>Hint 2</summary>

Clip x to [-2.5, 2.5], then divide by 5 and add 0.5. Wait, let me recalculate: if x is in [-2.5, 2.5], then (x + 2.5) / 5 maps to [0, 1].

</details>

<details>
<summary>Hint 3</summary>

np.clip(x, -2.5, 2.5) gives the linear region. Then transform.

</details>

## Theory

Hard Sigmoid is a computationally efficient approximation to sigmoid. The sigmoid curve is flattened to three regions: zero for large negative x, linear for x near zero, and one for large positive x.

This reduces computation from an exponential to simple comparisons and a linear operation.

## Explanation

The solution clips input to [-2.5, 2.5], shifts by 2.5 to get [0, 5], then divides by 5 to get [0, 1]:

```python
return (np.clip(x, -2.5, 2.5) + 2.5) / 5.0
```

Inputs are not modified. The result is a new array.
