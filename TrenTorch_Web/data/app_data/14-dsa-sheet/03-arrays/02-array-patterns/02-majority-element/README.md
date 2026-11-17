---
name: sheet-majority-element
title: 'Majority Element'
tags: [dsa-sheet, arrays, array-patterns]
difficulty: Intermediate
theory: the-majority-vote
---

## Statement

Return the value that appears **more than `len(nums) / 2` times**. If no value does, return `-1`.

### Examples

**Example 1**

Input:

```python
majority_element([2, 2, 1, 1, 2, 2, 3])
```

Output:

```text
2
```

`2` appears 4 times out of 7.

**Example 2**

Input:

```python
majority_element([1, 2, 3])
```

Output:

```text
-1
```

No value appears more than 1.5 times.

### Constraints

- `0 <= len(nums) <= 3 * 10**5`
- `0 <= nums[i] <= 10**9`

## Explanation

The first loop finds the candidate by voting. The second counts how often it occurs and returns it only if that is more than `n // 2`; otherwise `-1`. Empty input has no candidate and returns `-1`.

### Complexity

- Time: O(n). Boyer-Moore voting is one pass, and a second pass verifies the candidate.
- Space: O(1). A candidate and a counter.
