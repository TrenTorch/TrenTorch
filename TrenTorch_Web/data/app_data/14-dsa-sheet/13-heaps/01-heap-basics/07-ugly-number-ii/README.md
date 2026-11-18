---
name: sheet-ugly-number-ii
title: 'The Nth Ugly Number'
tags: [dsa-sheet, heaps, heap-basics]
difficulty: Intermediate
theory: growing-numbers-from-smaller-ones
---

## Statement

An **ugly number** is a positive whole number whose only prime factors are `2`, `3` and `5`. The first ones are `1, 2, 3, 4, 5, 6, 8, 9, 10, 12, ...`. Return the **`n`-th** ugly number (`n = 1` gives `1`).

For `n = 10` the answer is `12`.

The starter code tests every whole number in turn. It is correct but too slow when `n` is large.

### Examples

**Example 1**

Input:

```python
nth_ugly_number(10)
```

Output:

```text
12
```

**Example 2**

Input:

```python
nth_ugly_number(1)
```

Output:

```text
1
```

### Constraints

- `1 <= n <= 100000`

## Explanation

`seen` keeps duplicates out of the heap. The loop pops `n - 1` numbers and the next pop is the answer; here the three-pointer version is shown because it is `O(n)`.

### Complexity

- Time: O(n). Three pointers build the sequence in order, one new number per step.
- Space: O(n). The list of ugly numbers.
