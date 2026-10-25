---
name: sheet-container-with-most-water
title: 'Container With Most Water'
tags: [dsa-sheet, two-pointers, two-pointers]
difficulty: Intermediate
---

## Statement

`heights[i]` is the height of a vertical line at position `i`. Choose **two lines** that, together with the x-axis, form a container, and return the **largest amount of water** it can hold: `min(height of the two lines) * distance between them`. The container cannot be tilted.

For `[1, 8, 6, 2, 5, 4, 8, 3, 7]` the answer is `49`.

The starter code tries every pair. It is correct but too slow for many lines.

### Examples

**Example 1**

Input:

```python
max_water([1, 8, 6, 2, 5, 4, 8, 3, 7])
```

Output:

```text
49
```

**Explanation:** The largest area uses the lines at indices 1 and 8 with heights 8 and 7; distance 7 gives area 8*7=49.

**Example 2**

Input:

```python
max_water([1, 1])
```

Output:

```text
1
```

**Explanation:** Two lines of height 1, distance 1, area 1*1=1.

### Constraints

- `0 <= len(heights) <= 200000`
- `0 <= heights[i] <= 10**4`

## Theory

**Two pointers** means keeping two positions in the data (often one at each end, or one behind the other) and moving them according to a rule, so that each position moves at most `n` times in total. That turns a double loop (`O(n²)`) into a single pass (`O(n)`).

Start with the **widest** container: pointers at both ends. Its area is limited by the **shorter** line. Which pointer should move? If you move the **taller** line inwards, the width shrinks and the height is still limited by the same shorter line, so the area cannot improve. So the shorter line is useless in every narrower container too, and you can safely **discard it**: move the pointer of the shorter line inwards.

Repeat, keeping the best area. `O(n)`. The reasoning "this choice can never be part of a better answer, so throw it away" is the heart of many two-pointer solutions.

## Explanation

Each step computes the area of the current pair and moves the pointer at the shorter line, since keeping it could only give smaller or equal areas.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                                         | Variables              |
| ----------------------------------------------------------------------- | ---------------------- |
| `left, right = 0, len(heights) - 1`                                     | `left = 0, right = 8`  |
| `best = max(best, min(heights[left], heights[right]) * (right - left))` | `best = 8`             |
| `left += 1`                                                             | `left = 1`             |
| `right -= 1`                                                            | `right = 7, best = 49` |
| `right -= 1`                                                            | `right = 5`            |
| `right -= 1`                                                            | `right = 3`            |
| `right -= 1`                                                            | `right = 2`            |
| `return`                                                                | `returned = 49`        |

### Complexity

- Time: O(n) (n is number of heights).
- Extra space: O(1) (only a few variables).
- The brute force takes O(n^2) (check all pairs).
