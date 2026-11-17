---
name: sheet-first-unique-character
title: 'First Unique Character'
tags: [dsa-sheet, hashing, counting-with-dictionaries]
difficulty: Beginner
theory: counting-letters
---

## Statement

Return the **index** of the first character in `s` that appears **exactly once** in the whole string, or `-1` if every character repeats (or the string is empty).

### Examples

**Example 1**

Input:

```python
first_unique_character('leetcode')
```

Output:

```text
0
```

`l` at index 0 appears once.

**Example 2**

Input:

```python
first_unique_character('aabb')
```

Output:

```text
-1
```

Every character repeats.

### Constraints

- `0 <= len(s) <= 3 * 10**5`
- `s` contains lower-case letters.

## Explanation

`counts = Counter(s)` records how often each character occurs. The loop over `enumerate(s)` returns the first index whose character has `counts[ch] == 1`. If the loop ends, no character is unique and the answer is `-1`.

### Complexity

- Time: O(n). One counting pass and one scan.
- Space: O(1). The counter has at most 26 letters.
