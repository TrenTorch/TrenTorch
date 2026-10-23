---
name: sheet-maximum-xor-of-two-numbers
title: 'Maximum XOR of Two Numbers'
tags: [dsa-sheet, bit-manipulation, bit-patterns]
difficulty: Mastery
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

## Theory

Build the answer **one bit at a time from the top**. Greedy idea: for the highest bit, can some pair xor to a number with that bit set? If yes, keep it, because a higher bit is worth more than all the lower bits together.

Keep a `best` answer so far. For each bit from 29 down to 0: take the **prefixes** of all numbers (`x >> bit`), put them in a set, and ask whether some prefix `p` has a partner `q` in the set with `p ^ q == candidate`, where `candidate = (best << 1) | 1` is `best` with the new bit tried as 1. Using `p ^ candidate in prefixes` is a constant-time test, because `p ^ q == candidate` exactly when `q == p ^ candidate`.

Each of the 30 rounds is `O(n)`, so the total is `O(30 n)`. The classic alternative stores the numbers in a **binary trie** and, for each number, walks down choosing the opposite bit whenever possible.

## Explanation

After processing bit `b`, `best` is the largest xor of the numbers' prefixes down to that bit. Trying `best * 2 + 1` asks whether the new bit can be 1; if some pair achieves it, `best` grows, otherwise it takes the bit as 0.
