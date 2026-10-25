---
name: sheet-trapping-rain-water
title: 'Trapping Rain Water'
tags: [dsa-sheet, two-pointers, two-pointers]
difficulty: Advanced
---

## Statement

`heights[i]` is the height of a bar of width 1. After it rains, water collects between the bars. Return the **total amount of water trapped**.

For `[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]` the answer is `6`.

The starter code searches both sides of every bar. It is correct but too slow for many bars.

### Examples

**Example 1**

Input:

```python
trap_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])
```

Output:

```text
6
```

**Explanation:** The dips of depths 2,3,1,1 units between the bars trap a total of 6 units of water.

**Example 2**

Input:

```python
trap_water([4, 2, 0, 3, 2, 5])
```

Output:

```text
9
```

**Explanation:** Between heights 4 and 5, bars of 2,0,3,2 trap 9 units: 2,2,3,2,0 units respectively. Sum 9.

### Constraints

- `0 <= len(heights) <= 200000`
- `0 <= heights[i] <= 10**5`

## Theory

The water above bar `i` has height `min(tallest bar to the left, tallest bar to the right) - heights[i]` (never below zero). Computing both tallest bars from scratch for every `i` costs `O(n²)`.

**Two pointers** means keeping two positions in the data (often one at each end, or one behind the other) and moving them according to a rule, so that each position moves at most `n` times in total. That turns a double loop (`O(n²)`) into a single pass (`O(n)`).

Keep `left_max` and `right_max`, the tallest bars seen so far from each end, with a pointer at each end. The side with the **smaller** max decides the water level on that side, because the other side already has a taller wall: so process that side's bar: water there is `its_max - height`, then move that pointer inwards.

`O(n)` time and `O(1)` memory. (A prefix-maximum array for each side also works with `O(n)` memory.)

## Explanation

When `left_max < right_max`, the water at `left` is limited by `left_max` no matter what is further right, since a wall at least as tall exists on the right. Symmetrically for the right side.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                              | Variables                                           |
| -------------------------------------------- | --------------------------------------------------- |
| `left, right = 0, len(heights) - 1`          | `left = 0, right = 11`                              |
| `left += 1`                                  | `left = 1, left_max = 0, right_max = 0, total = 0`  |
| `left += 1`                                  | `left = 2, right = 10, left_max = 1, right_max = 1` |
| `right_max = max(right_max, heights[right])` | `left = 3, right_max = 2, total = 1`                |
| `right -= 1`                                 | `right = 8, total = 2`                              |
| `left += 1`                                  | `left = 4, right = 7, left_max = 2`                 |
| `left += 1`                                  | `left = 6, total = 5`                               |
| `return`                                     | `returned = 6`                                      |

### Complexity

- Time: O(n) - n is number of bars.
- Extra space: O(1) - constant extra space.
- The brute force takes O(n^2) - nested loops over bars.
