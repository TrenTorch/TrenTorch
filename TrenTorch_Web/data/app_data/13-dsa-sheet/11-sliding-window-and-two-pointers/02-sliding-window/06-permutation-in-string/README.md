---
name: sheet-permutation-in-string
title: 'Permutation in a String'
tags: [dsa-sheet, sliding-window, sliding-window]
difficulty: Intermediate
---

## Statement

Return `True` if `s2` contains a **permutation of `s1`**: some substring of `s2` has exactly the same letters as `s1`, in any order. `"ab"` is inside `"eidbaooo"` (as `"ba"`); it is not inside `"eidboaoo"`.

### Examples

**Example 1**

Input:

```python
check_inclusion('ab', 'eidbaooo')
```

Output:

```text
True
```

**Example 2**

Input:

```python
check_inclusion('ab', 'eidboaoo')
```

Output:

```text
False
```

### Constraints

- `0 <= len(s1) <= 100000`
- `0 <= len(s2) <= 200000`
- Lower-case letters.

## Theory

A **sliding window** is a range `[left, right]` of the data that grows on the right and shrinks on the left. Because each end only moves forward, the whole pass is `O(n)`, while the window always describes one candidate subarray or substring.

The window has a **fixed size**, `len(s1)`. Two strings are rearrangements of each other when their **letter counts** are equal. So slide a window of that size over `s2`, keeping a count of the window's letters, and compare it with the count of `s1`.

Comparing two 26-entry counts costs `O(26)` per step, which is constant. Update the counts in `O(1)` per slide: add the new letter on the right, remove the old letter on the left. Total `O(26 * n)`.

## Explanation

`need` is the count of `s1`. `window` is the count of the current window of `s2`; after each slide they are compared.
