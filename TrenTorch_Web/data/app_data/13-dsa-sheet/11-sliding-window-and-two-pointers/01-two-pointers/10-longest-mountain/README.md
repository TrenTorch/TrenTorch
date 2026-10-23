---
name: sheet-longest-mountain
title: 'Longest Mountain in an Array'
tags: [dsa-sheet, two-pointers, two-pointers]
difficulty: Intermediate
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

## Theory

**Two pointers** means keeping two positions in the data (often one at each end, or one behind the other) and moving them according to a rule, so that each position moves at most `n` times in total. That turns a double loop (`O(n²)`) into a single pass (`O(n)`).

Each mountain has a peak. Scan for positions where `arr[i - 1] < arr[i] > arr[i + 1]`, and from such a peak **expand outwards**: a left pointer goes down while the values keep decreasing to the left, a right pointer goes down while they keep decreasing to the right. The mountain is `right - left + 1` long.

A cleverer scan jumps `i` to `right` after each mountain, so every element is read a constant number of times: `O(n)`. (Just advancing `i` by 1 can revisit the same slope many times in some inputs, which is why you skip.)

## Explanation

After a peak is found and expanded, `i` continues from `right`, because no element before `right` can be the peak of a longer mountain that also starts inside this one.
