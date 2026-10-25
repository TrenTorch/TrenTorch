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

**Explanation:** The maximum XOR value of 28 is obtained by selecting 5 and 25 from the list.

**Example 2**

Input:

```python
max_xor_pair([7])
```

Output:

```text
0
```

**Explanation:** With only one element, 7, the only possible pair is with itself, resulting in a XOR of 0.

### Constraints

- `1 <= len(nums) <= 50000`
- `0 <= nums[i] < 2**30`

## Theory

Build the answer **one bit at a time from the top**. Greedy idea: for the highest bit, can some pair xor to a number with that bit set? If yes, keep it, because a higher bit is worth more than all the lower bits together.

Keep a `best` answer so far. For each bit from 29 down to 0: take the **prefixes** of all numbers (`x >> bit`), put them in a set, and ask whether some prefix `p` has a partner `q` in the set with `p ^ q == candidate`, where `candidate = (best << 1) | 1` is `best` with the new bit tried as 1. Using `p ^ candidate in prefixes` is a constant-time test, because `p ^ q == candidate` exactly when `q == p ^ candidate`.

Each of the 30 rounds is `O(n)`, so the total is `O(30 n)`. The classic alternative stores the numbers in a **binary trie** and, for each number, walks down choosing the opposite bit whenever possible.

## Explanation

After processing bit `b`, `best` is the largest xor of the numbers' prefixes down to that bit. Trying `best * 2 + 1` asks whether the new bit can be 1; if some pair achieves it, `best` grows, otherwise it takes the bit as 0.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                       | Variables                                                       |
| ------------------------------------- | --------------------------------------------------------------- |
| `best = 0`                            | `best = 0`                                                      |
| `for bit in range(29, -1, -1):`       | `bit = 25, prefixes = {0}, candidate = 1`                       |
| `for bit in range(29, -1, -1):`       | `bit = 18`                                                      |
| `for bit in range(29, -1, -1):`       | `bit = 11`                                                      |
| `for bit in range(29, -1, -1):`       | `bit = 4`                                                       |
| `best = candidate`                    | `best = 3, bit = 3, prefixes = {0, 1, 3}, candidate = 3`        |
| `prefixes = {x >> bit for x in nums}` | `best = 7, bit = 1, prefixes = {1, 2, 4, 5, 12}, candidate = 7` |
| `return`                              | `returned = 28`                                                 |

### Complexity

- Time: O(n) where n is the length of nums.
- Extra space: O(n) where n is the length of nums.
- The brute force takes O(n^2) where n is the length of nums.
