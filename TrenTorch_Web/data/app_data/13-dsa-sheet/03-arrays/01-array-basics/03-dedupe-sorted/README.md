---
name: sheet-dedupe-sorted
title: 'Remove Duplicates From Sorted'
tags: [dsa-sheet, arrays, array-basics]
difficulty: Beginner
---

## Statement

`nums` is sorted in non-decreasing order. Return a new list with each value kept **once**, still in order. Do not use `set`: use the fact that the list is sorted.

### Examples

**Example 1**

Input:

```python
dedupe_sorted([1, 1, 2, 2, 2, 3])
```

Output:

```text
[1, 2, 3]
```

**Explanation:** The sorted input has consecutive duplicates; the algorithm appends each value only when it differs from the last kept value, yielding [1, 2, 3].

**Example 2**

Input:

```python
dedupe_sorted([4, 4, 4])
```

Output:

```text
[4]
```

**Explanation:** All elements are 4, so only the first 4 is added to the output list, resulting in [4].

### Constraints

- `0 <= len(nums) <= 3 * 10**5`
- `nums` is sorted in non-decreasing order.

## Theory

In a sorted list, equal values sit **next to each other**. So you never need to remember every value you have seen (which is what a `set` does). It is enough to compare each value with the **last one you kept**: if it differs, keep it; if it is the same, skip it.

This is the **two-pointer** idea: one pointer reads every value, and another marks where the next kept value goes. In Python the "write pointer" is simply the end of the result list. It runs in `O(n)` time and needs no hashing.

## Explanation

`out[-1]` is the last kept value. A new value is appended only when `out` is empty or the value differs from `out[-1]`. Sortedness guarantees that a repeated value is always adjacent to its twin.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line  | Variables              |
| ---------------- | ---------------------- |
| `out = []`       | `out = []`             |
| `for x in nums:` | `x = 1`                |
| `out.append(x)`  | `out = [1]`            |
| `for x in nums:` | `x = 2`                |
| `out.append(x)`  | `out = [1, 2]`         |
| `for x in nums:` | `x = 3`                |
| `out.append(x)`  | `out = [1, 2, 3]`      |
| `return`         | `returned = [1, 2, 3]` |

### Complexity

- Time: O(n) time, n is length of nums.
- Extra space: O(n) extra space for output list.
- The brute force takes O(n log n) time, n is length of nums.
