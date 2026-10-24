---
name: sheet-lcm-of-list
title: 'Least Common Multiple of a List'
tags: [dsa-sheet, basics, python-toolbox]
difficulty: Beginner
---

## Statement

Return the **least common multiple** (LCM) of all numbers in `nums`: the smallest positive integer that every number divides evenly. The LCM of an empty list is `1`.

### Examples

**Example 1**

Input:

```python
lcm_of_list([4, 6, 10])
```

Output:

```text
60
```

60 is the smallest number that 4, 6 and 10 all divide.

**Example 2**

Input:

```python
lcm_of_list([])
```

Output:

```text
1
```

### Constraints

- `0 <= len(nums) <= 200`
- `1 <= nums[i] <= 10**12`
- The answer can have thousands of digits.

## Theory

The greatest common divisor (GCD) and LCM are linked: `lcm(a, b) = a * b // gcd(a, b)`. Python has both in `math`: `math.gcd` and, since Python 3.9, `math.lcm`, which accepts any number of arguments.

To fold a list down to one value, `functools.reduce(f, items, start)` applies `f` to the running result and each next item. With `start = 1` an empty list falls out naturally as `1`.

Python integers have no size limit, so the result can be as big as memory allows. That is a big advantage over languages with 64-bit integers, where this problem needs modular arithmetic or big-number classes.

## Explanation

`reduce(math.lcm, nums, 1)` combines the values one at a time. Because `math.lcm(x, y)` is exact for any size, there is no overflow to worry about.
