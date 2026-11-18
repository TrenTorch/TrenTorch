---
name: sheet-frequency-extremes
title: 'Most and Least Frequent Value'
tags: [dsa-sheet, hashing, counting-with-dictionaries]
difficulty: Beginner
theory: picking-the-winner-and-breaking-ties
---

## Statement

Return `[most, least]`: the value that appears **most often** and the value that appears **least often** in `nums`. If several values tie, take the **smaller value**.

### Examples

**Example 1**

Input:

```python
frequency_extremes([4, 4, 5, 5, 6])
```

Output:

```text
[4, 6]
```

`4` and `5` both appear twice; the smaller is 4. `6` appears once.

**Example 2**

Input:

```python
frequency_extremes([7])
```

Output:

```text
[7, 7]
```

One value is both the most and the least frequent.

### Constraints

- `1 <= len(nums) <= 3 * 10**5`
- `-10**9 <= nums[i] <= 10**9`

## Explanation

`counts` maps each value to its frequency. `min(counts, key=lambda v: (-counts[v], v))` is the value with the biggest count, smallest on ties. `min(counts, key=lambda v: (counts[v], v))` is the value with the smallest count, smallest on ties.

### Complexity

- Time: O(n). One counting pass plus two scans of the `d <= n` distinct values.
- Space: O(d). The counter holds `d` distinct values.
