---
name: sheet-permutation-in-string
title: 'Permutation in a String'
tags: [dsa-sheet, sliding-window, sliding-window]
difficulty: Intermediate
theory: windows-of-letter-counts
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

## Explanation

`need` is the count of `s1`. `window` is the count of the current window of `s2`; after each slide they are compared.

### Complexity

- Time: O(n). The window moves one step at a time and comparing two 26-letter counts is O(26).
- Space: O(1). Two arrays of 26 counts.
