---
name: sheet-maximum-xor-of-two-numbers
title: 'Maximum XOR of Two Numbers'
tags: [dsa-sheet, bit-manipulation, bit-patterns]
difficulty: Mastery
theory: the-same-idea-with-a-set-of-prefixes
---

## Statement

Return the **maximum value of `a ^ b`** over two numbers `a` and `b` taken from `nums` (they can be the same element, so a list with one number gives `0`).

The starter code tries every pair. It is correct but too slow for long lists.

### Examples

**Example 1**

Input:

```python
max_xor_pair([3, 10, 5, 25, 2, 8])
```

Output:

```text
28
```

**Example 2**

Input:

```python
max_xor_pair([7])
```

Output:

```text
0
```

### Constraints

- `1 <= len(nums) <= 50000`
- `0 <= nums[i] < 2**30`

## Explanation

After processing bit `b`, `best` is the largest xor of the numbers' prefixes down to that bit. Trying `best * 2 + 1` asks whether the new bit can be 1; if some pair achieves it, `best` grows, otherwise it takes the bit as 0.

### Complexity

- Time: O(30 * n). The answer is built one bit at a time from the top; each bit needs one pass over the prefixes with O(1) set lookups.
- Space: O(n). The set of prefixes.
