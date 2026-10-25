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

**Explanation:** The peak 7 is reached by the rise 1, 4, 7 and left by the fall 7, 3, 2. That mountain has 5 values. The final 5 only rises from 2, so it is not a peak.

**Example 2**

Input:

```python
longest_mountain([2, 2, 2])
```

Output:

```text
0
```

**Explanation:** All the values are equal, so nothing strictly rises or falls and there is no mountain: 0.

### Constraints

- `0 <= len(arr) <= 200000`
- `0 <= arr[i] <= 10**9`

## Theory

**Two pointers** means keeping two positions in the data (often one at each end, or one behind the other) and moving them according to a rule, so that each position moves at most `n` times in total. That turns a double loop (`O(n²)`) into a single pass (`O(n)`).

Each mountain has a peak. Scan for positions where `arr[i - 1] < arr[i] > arr[i + 1]`, and from such a peak **expand outwards**: a left pointer goes down while the values keep decreasing to the left, a right pointer goes down while they keep decreasing to the right. The mountain is `right - left + 1` long.

A cleverer scan jumps `i` to `right` after each mountain, so every element is read a constant number of times: `O(n)`. (Just advancing `i` by 1 can revisit the same slope many times in some inputs, which is why you skip.)

## Explanation

After a peak is found and expanded, `i` continues from `right`, because no element before `right` can be the peak of a longer mountain that also starts inside this one.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                      | Variables         |
| ------------------------------------ | ----------------- |
| `n = len(arr)`                       | `n = 7`           |
| `i = 1`                              | `best = 0, i = 1` |
| `i += 1`                             | `i = 2`           |
| `left = i - 1`                       | `i = 3, left = 2` |
| `left -= 1`                          | `left = 1`        |
| `right += 1`                         | `right = 5`       |
| `best = max(best, right - left + 1)` | `best = 5`        |
| `return`                             | `returned = 5`    |

### Complexity

- Time: O(n) time, n is array length.
- Extra space: O(1) extra space.
- The brute force takes O(n^3) time, n is array length.
