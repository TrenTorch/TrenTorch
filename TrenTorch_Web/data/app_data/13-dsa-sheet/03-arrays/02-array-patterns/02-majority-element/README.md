---
name: sheet-majority-element
title: 'Majority Element'
tags: [dsa-sheet, arrays, array-patterns]
difficulty: Intermediate
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

## Theory

A `Counter` solves this in `O(n)` time but `O(n)` memory. The **Boyer-Moore voting** algorithm needs only two variables.

Keep a `candidate` and a `count`. For each value: if `count` is `0`, adopt the value as the candidate; then add one to `count` if the value equals the candidate, otherwise subtract one. Each different value "cancels" one vote of the candidate. A value that appears more than half the time has more votes than all the others combined, so it cannot be fully cancelled and ends as the candidate.

The algorithm only guarantees that a majority value, **if there is one**, is the final candidate. It never tells you whether one exists, so finish with a second pass that counts the candidate.

## Explanation

The first loop finds the candidate by voting. The second counts how often it occurs and returns it only if that is more than `n // 2`; otherwise `-1`. Empty input has no candidate and returns `-1`.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                        | Variables                  |
| -------------------------------------- | -------------------------- |
| `candidate = None`                     | `candidate = None`         |
| `for x in nums:`                       | `count = 0, x = 2`         |
| `count += 1 if x == candidate else -1` | `candidate = 2, count = 1` |
| `for x in nums:`                       | `count = 2, x = 1`         |
| `count += 1 if x == candidate else -1` | `count = 0`                |
| `count += 1 if x == candidate else -1` | `count = 1, x = 2`         |
| `for x in nums:`                       | `count = 2, x = 3`         |
| `return`                               | `returned = 2`             |

### Complexity

- Time: O(n) where n is len(nums).
- Extra space: O(1) extra memory.
- The brute force takes O(n^2) where n is len(nums).
