---
name: sheet-max-points-on-a-line
title: 'Max Points on a Line'
tags: [dsa-sheet, maths, counting-and-digits]
difficulty: Advanced
---

## Statement

`points[i] = [x, y]` are **different** points on a plane. Return the **largest number of points that lie on the same straight line**.

For `[[1, 1], [2, 2], [3, 3]]` the answer is `3`; for `[[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]]` it is `4`.

The starter code tests every triple of points. It is correct but too slow for many points.

### Examples

**Example 1**

Input:

```python
max_points([[1, 1], [2, 2], [3, 3]])
```

Output:

```text
3
```

**Example 2**

Input:

```python
max_points([[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]])
```

Output:

```text
4
```

### Constraints

- `0 <= len(points) <= 300`
- `0 <= x, y <= 10000`
- All points are different.

## Theory

Many contest problems are about **numbers**, and the input is huge (up to `10^12` or more), so a loop up to `n` is far too slow. The tools: the **square root bound** (a number `n` has a divisor `<= sqrt(n)` unless it is prime), **modular arithmetic** (work with remainders so the numbers stay small), and **formulas** that replace a loop. Python's big integers make the arithmetic itself safe, but the number of steps is what you must control.

Fix a point `p`. Every other point `q` defines a **direction** from `p`; points on the same line through `p` share the same direction. Group the other points by direction and take the largest group (plus `p` itself). Repeat for every `p`.

Directions must be compared **exactly**. Floating-point slopes (`dy / dx`) can be wrong for close directions and fail for vertical lines. Use the integer pair `(dy, dx)` **divided by their gcd**, and fix the sign (make `dx` positive, or `dy` positive when `dx` is 0) so that opposite directions along the same line give the same key. `O(n²)` with a dictionary per point.

## Explanation

`slopes` counts points by normalised direction from the current point. The best line through it has `max(slopes.values()) + 1` points.
