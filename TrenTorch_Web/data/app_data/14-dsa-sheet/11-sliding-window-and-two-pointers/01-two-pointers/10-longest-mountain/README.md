---
name: sheet-longest-mountain
title: 'Longest Mountain in an Array'
tags: [dsa-sheet, two-pointers, two-pointers]
difficulty: Intermediate
theory: the-longest-mountain
---

## Statement

A **mountain** is a run of at least 3 consecutive values that **strictly increases** to a peak and then **strictly decreases**. Return the length of the longest mountain in `arr`, or `0` if there is none.

For `[2, 1, 4, 7, 3, 2, 5]` the answer is `5` (`[1, 4, 7, 3, 2]`).

### Examples

**Example 1**

Input:

```python
longest_mountain([2, 1, 4, 7, 3, 2, 5])
```

Output:

```text
5
```

**Example 2**

Input:

```python
longest_mountain([2, 2, 2])
```

Output:

```text
0
```

### Constraints

- `0 <= len(arr) <= 200000`
- `0 <= arr[i] <= 10**9`

## Explanation

After a peak is found and expanded, `i` continues from `right`, because no element before `right` can be the peak of a longer mountain that also starts inside this one.

### Complexity

- Time: O(n). Every element is visited a constant number of times because the scan resumes after each mountain.
- Space: O(1). A few indices.
