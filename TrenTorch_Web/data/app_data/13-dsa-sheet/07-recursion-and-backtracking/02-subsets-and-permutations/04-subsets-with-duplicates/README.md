---
name: sheet-subsets-with-duplicates
title: 'Subsets With Repeated Values'
tags: [dsa-sheet, recursion, subsets-and-permutations]
difficulty: Intermediate
---

## Statement

`nums` may contain **repeated values**. Return every **different subset** (two subsets are the same if they hold the same values with the same counts). Write each subset in increasing order and list the subsets in dictionary order.

For `[1, 2, 2]`: `[], [1], [1, 2], [1, 2, 2], [2], [2, 2]`.

### Examples

**Example 1**

Input:

```python
subsets_with_duplicates([1, 2, 2])
```

Output:

```text
[[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]
```

**Explanation:** The sorted array is [1,2,2]. Backtracking generates unique subsets by skipping duplicate 2s at the same level, yielding subsets in lexicographic order: empty, then with 1, then with 2, then with two 2s.

**Example 2**

Input:

```python
subsets_with_duplicates([0])
```

Output:

```text
[[], [0]]
```

**Explanation:** For a single element, the only subsets are the empty set and the set containing that element, which are already in increasing order.

### Constraints

- `0 <= len(nums) <= 14`
- `-100 <= nums[i] <= 100`

## Theory

Take the subsets recursion for different values and ask where the duplicates come from. With `[1, 2, 2]`, choosing the first `2` or the second `2` gives the same subset, so the answer would list `[1, 2]` twice.

The fix: **sort**, so equal values sit next to each other, and then in each loop over candidates **skip a value that equals the previous candidate at the same level**: `if j > start and a[j] == a[j - 1]: continue`. The condition `j > start` is important. It means "this value was already tried as the first pick in _this_ loop", but it still allows a repeated value to be used _deeper_ in the recursion (taking the second `2` after the first one is a different subset, `[2, 2]`).

Skipping duplicates at the same level of the recursion is the standard way to avoid repeated answers in backtracking.

## Explanation

The loop starts at `start`. A value equal to the one before it **within the same loop** is skipped because that choice would build exactly the same subsets as the earlier one. Values further down the recursion start a new loop, so a second equal value can still be taken after the first.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line           | Variables                                                           |
| ------------------------- | ------------------------------------------------------------------- |
| `a = sorted(nums)`        | `a = [1, 2, 2]`                                                     |
| `out = []`                | `out = []`                                                          |
| `def go(start, current):` | `go = <function subsets_with_duplicates.<locals>.go at 0x000001...` |
| `go(0, [])`               | `out = [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]`                   |
| `return`                  | `returned = [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]`              |

### Complexity

- Time: O(n * 2^n) where n is length of nums.
- Extra space: O(n) for recursion stack and current list.
- The brute force takes O(n * 2^n) where n is len(nums).
