---
name: sheet-sort-colors
title: 'Sort Zeros, Ones and Twos'
tags: [dsa-sheet, sorting, divide-and-conquer]
difficulty: Intermediate
---

## Statement

A list contains only the values `0`, `1` and `2` (think of three paint colours). Return it sorted in increasing order, without using a general-purpose sort.

A fast solution reads the list **once**. The tests can only check the answer, not how you got it, so the walkthrough after you solve it shows the one-pass idea. Aim for it anyway: it is a classic.

### Examples

**Example 1**

Input:

```python
sort_colors([2, 0, 2, 1, 1, 0])
```

Output:

```text
[0, 0, 1, 1, 2, 2]
```

**Example 2**

Input:

```python
sort_colors([1, 0])
```

Output:

```text
[0, 1]
```

### Constraints

- `0 <= len(nums) <= 10**6`
- Every `nums[i]` is `0`, `1` or `2`.

## Theory

When the values come from a tiny range you do not need comparisons at all. **Counting sort** counts how many `0`s, `1`s and `2`s there are, then writes them out in order: two passes, `O(n)`.

The **Dutch national flag** method does it in one pass with three pointers. `low` marks the end of the zeros, `high` marks the start of the twos, and `i` scans the middle. A `0` is swapped to `low`, a `2` is swapped to `high`, and a `1` stays. Everything before `low` is zero, everything after `high` is two, and the part between `low` and `i` is ones.

The lesson: a general sort costs `O(n log n)` because it must compare. If you know more about the data, you can beat that bound.

## Explanation

The counting version is shortest in Python: `counts = [nums.count(0), nums.count(1), nums.count(2)]` and rebuild with `[0] * c0 + [1] * c1 + [2] * c2`. Each `count` is a fast built-in pass.

The one-pass version: `low = i = 0`, `high = n - 1`. While `i <= high`: if `nums[i] == 0` swap it with `nums[low]` and advance both `low` and `i`; if it is `2` swap it with `nums[high]` and decrease `high` (do not advance `i`, the swapped-in value is not checked yet); if it is `1` just advance `i`.
