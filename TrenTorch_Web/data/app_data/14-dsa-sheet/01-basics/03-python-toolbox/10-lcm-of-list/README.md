---
name: sheet-lcm-of-list
title: 'Least Common Multiple of a List'
tags: [dsa-sheet, basics, python-toolbox]
difficulty: Beginner
theory: maths-helpers-and-big-numbers
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

## Explanation

`reduce(math.lcm, nums, 1)` combines the values one at a time. Because `math.lcm(x, y)` is exact for any size, there is no overflow to worry about.

### Complexity

- Time: O(n * B). `n` gcd steps; each divides the running lcm (at most `B = n * log2(max)` bits) by a number of at most 40 bits.
- Space: O(B). The running lcm is the only large value.
