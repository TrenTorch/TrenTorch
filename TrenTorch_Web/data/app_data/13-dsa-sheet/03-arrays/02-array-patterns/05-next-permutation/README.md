---
name: sheet-next-permutation
title: 'Next Permutation'
tags: [dsa-sheet, arrays, array-patterns]
difficulty: Advanced
---

## Statement

Arrangements of the same values can be listed in **dictionary order** (the order you would find them in a dictionary: compare the first value, then the second, and so on). Return the arrangement that comes **right after** `nums`. If `nums` is already the last one (all values from largest to smallest), return the first one: the values sorted in increasing order.

Repeated values are allowed, and the next arrangement must differ from the current one unless all values are equal.

### Examples

**Example 1**

Input:

```python
next_permutation([1, 2, 3])
```

Output:

```text
[1, 3, 2]
```

The next arrangement after 1, 2, 3 is 1, 3, 2.

**Example 2**

Input:

```python
next_permutation([3, 2, 1])
```

Output:

```text
[1, 2, 3]
```

This is the last arrangement, so it wraps to the first: 1, 2, 3.

### Constraints

- `1 <= len(nums) <= 2 * 10**5`
- `0 <= nums[i] <= 10**9`

## Theory

You cannot generate all arrangements: there are `n!` of them. Instead reason about _which_ positions change. Look at the end of the list. The longest suffix that is in **non-increasing** order (like `5 4 4 1`) is already the largest arrangement of its own values, so nothing inside the suffix can be increased.

So the change has to happen just **before** that suffix, at position `i`, the last place where `nums[i] < nums[i + 1]`. To get the smallest possible increase, swap `nums[i]` with the **smallest value in the suffix that is bigger than it** (scanning from the right finds it, because the suffix is non-increasing). Finally the suffix is still non-increasing, which is its largest order, so **reverse** it to make it as small as possible.

If no such `i` exists the whole list is non-increasing, which is the last arrangement; reversing it gives the first. Everything is `O(n)` time and `O(1)` extra space.

## Explanation

Find `i`, the rightmost index with `a[i] < a[i + 1]`. If there is none, reverse the whole list. Otherwise find the rightmost `j` with `a[j] > a[i]`, swap `a[i]` and `a[j]`, and reverse `a[i + 1:]`. Using `>=` and `<=` carefully (strict comparisons) handles repeated values.
