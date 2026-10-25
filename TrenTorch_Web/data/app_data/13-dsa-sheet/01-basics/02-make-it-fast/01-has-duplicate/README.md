---
name: sheet-has-duplicate
title: 'Has Duplicate'
tags: [dsa-sheet, basics, make-it-fast]
difficulty: Beginner
---

## Statement

Given a list of integers `nums`, return `True` if some value appears at least twice, and `False` if every value is different.

The starter code is correct, but it compares every pair of values, which is too slow for long lists. Make it fast.

### Examples

**Example 1**

Input:

```python
has_duplicate([1, 2, 3, 1])
```

Output:

```text
True
```

**Explanation:** The value 1 occurs twice, so the function returns true.

**Example 2**

Input:

```python
has_duplicate([1, 2, 3, 4])
```

Output:

```text
False
```

**Explanation:** The list contains four distinct values, so the function returns false.

### Constraints

- `1 <= len(nums) <= 2 * 10**5`
- `-10**9 <= nums[i] <= 10**9`

## Theory

Comparing every pair is `O(n²)`: `2 * 10⁵` numbers means about `2 * 10¹⁰` comparisons, far too many for one second.

The fix is a trade of memory for time. A `set` answers "have I seen this value?" in `O(1)` on average, because it stores values by a hash (a number computed from the value that tells where to look). Walk the list once, and stop at the first value already in the set. That is `O(n)` time and `O(n)` extra memory.

## Explanation

Keep a set of values seen so far. For each value, if it is already in the set the answer is `True`; otherwise add it. If the loop ends, every value was new.

A shorter version compares sizes: `len(set(nums)) != len(nums)`. It does the same work, but it always builds the whole set even when the first two values are equal.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line  | Variables              |
| ---------------- | ---------------------- |
| `seen = set()`   | `seen = set()`         |
| `for x in nums:` | `x = 1`                |
| `seen.add(x)`    | `seen = {1}`           |
| `for x in nums:` | `x = 2`                |
| `for x in nums:` | `seen = {1, 2}, x = 3` |
| `seen.add(x)`    | `seen = {1, 2, 3}`     |
| `for x in nums:` | `x = 1`                |
| `return`         | `returned = True`      |

### Complexity

- Time: O(n) where n is the length of nums.
- Extra space: O(n) for the set of seen values.
- The brute force takes O(n^2) where n is the length of nums.
