---
name: potd-brightness-dial-sigmoid
title: 'THE BRIGHTNESS DIAL'
tags: [activation-functions]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** Activation Functions

---

### Story

Adobe's auto-brightness tool squashes an unbounded adjustment score into `(0, 1)` before applying it
as a blend factor: sigmoid, forward and backward, exactly as every deep learning framework
implements it.

---

### The Math

```
sigma(x)  = 1 / (1 + e^-x)
sigma'(x) = sigma(x) * (1 - sigma(x))
```

### Input Format

```
n
x_1 ... x_n
```

### Output Format

Two lines: `sigma(x)` and `sigma'(x)`, 6 decimals each.

### Constraints

- `1 <= n <= 10^5`, `|x_i| <= 50`
- Time limit: 1.0 second.

---

### Example

**Input**

```
1
0.5
```

**Output**

```
0.622459
0.235004
```

## Theory

### The simple version

Sigmoid squashes any real number into a value between 0 and 1, so it reads like a probability. Large positive inputs get squeezed toward 1, large negative inputs toward 0, and 0 itself lands exactly in the middle.

### The naive formula overflows

`1 / (1 + e^-x)` computes `e^-x` directly, and for a very negative `x` (down to `-50` here),
`e^-x` is an astronomically large number that overflows to infinity in floating point, before the
division ever happens. The formula is mathematically fine; the direct evaluation of it is not, at
this range.

### The overflow-safe rewrite

For `x >= 0`, `1 / (1 + e^-x)` is safe (`e^-x` shrinks toward `0`). For `x < 0`, use the algebraically
equivalent `e^x / (1 + e^x)` instead, where `e^x` shrinks toward `0` rather than growing. Branching
on the sign of `x` and picking whichever form keeps the exponent negative is what separates a
"textbook correct" implementation from one that silently produces `inf`/`nan` on this problem's
large-magnitude hidden tests.

### `x = 0` is the midpoint by construction

At `x = 0` both forms agree exactly: `sigma(0) = 0.5`, `sigma'(0) = 0.5 * 0.5 = 0.25`.

## Explanation

`sigmoid_forward` applies `np.where(x >= 0, 1/(1+exp(-x)), exp(x)/(1+exp(x)))`, computing both
branches vectorized and selecting per-element with the sign of `x`, so every element of the batch
gets whichever of the two algebraically-equivalent forms keeps its own exponent negative,
regardless of what any other element in the batch needs. The derivative is then computed from the
already-safe `sigma(x)` values with `sigma * (1 - sigma)`, which never touches `exp` again.
