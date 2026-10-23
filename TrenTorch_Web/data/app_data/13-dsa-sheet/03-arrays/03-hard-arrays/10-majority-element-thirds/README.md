---
name: sheet-majority-element-thirds
title: 'Elements Appearing More Than n/3 Times'
tags: [dsa-sheet, arrays, hard-arrays]
difficulty: Advanced
---

## Statement

Return all the values that appear **more than `len(nums) / 3` times**, as a sorted list (each value once). There can be at most two such values. Return `[]` if there are none.

### Examples

**Example 1**

Input:

```python
majority_element_thirds([3, 2, 3])
```

Output:

```text
[3]
```

`3` appears 2 times and `2` once. `n / 3` is 1, so only `3` qualifies.

**Example 2**

Input:

```python
majority_element_thirds([1, 2, 3, 4])
```

Output:

```text
[]
```

Each value appears once, which is not more than `4 / 3`.

### Constraints

- `0 <= len(nums) <= 3 * 10**5`
- `0 <= nums[i] <= 10**9`

## Theory

A `Counter` gives the answer in `O(n)` time and `O(n)` memory. The **Boyer-Moore voting** idea extends to this problem and needs just a few variables.

Why at most two? If three different values each appeared more than `n / 3` times, together they would exceed `n`. So keep **two candidates** with two counters. For each value: if it equals a candidate, add a vote to that candidate; otherwise if a counter is `0`, adopt the value as a new candidate with one vote; otherwise **every** candidate loses a vote (the new value cancels one vote from each of them and from itself).

As with the simple majority, this finds only the _possible_ answers. A second pass must count the two candidates and keep those with more than `n // 3` occurrences.

## Explanation

The first loop is the voting. The check order matters: first match an existing candidate, then fill an empty slot, then decrement both. The second pass counts each candidate and keeps those with `count * 3 > n`. Sorting the (at most two) results gives the required order.
