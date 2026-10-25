---
name: sheet-min-flips-to-make-or
title: 'Minimum Flips to Make a OR b Equal c'
tags: [dsa-sheet, bit-manipulation, bit-patterns]
difficulty: Intermediate
---

## Statement

Return the **minimum number of bit flips** in `a` and `b` (a flip changes one bit of one of them) so that `a | b == c`.

For `a = 2`, `b = 6`, `c = 5` the answer is `3`.

### Examples

**Example 1**

Input:

```python
min_flips(2, 6, 5)
```

Output:

```text
3
```

**Explanation:** Bit 0 needs one flip (both 0, target 1), bit 1 needs two flips (both 1, target 0), bit 2 matches; total 3.

**Example 2**

Input:

```python
min_flips(4, 2, 7)
```

Output:

```text
1
```

**Explanation:** Only bit 0 has both a and b zero while c is one, requiring one flip; other bits already satisfy a|b=c.

### Constraints

- `0 <= a, b, c < 2**31`

## Theory

Positions are independent: look at each bit position `i` and the three bits `x`, `y` of `a`, `b` and `z` of `c`.

- If `z == 0`, both `x` and `y` must become `0`: you flip each one that is `1` (up to 2 flips).
- If `z == 1`, at least one of `x`, `y` must be `1`: if both are `0` you need 1 flip, otherwise 0.

Add up the flips over the 31 positions. The shortcut with masks: `needed = (a | b) ^ c` marks the positions where the OR is wrong. Where `c` is 0, the wrong positions cost `a_bit + b_bit` flips; where `c` is 1, they cost 1 flip.

## Explanation

The loop runs over bit positions and applies the case analysis above. Positions where `a | b` already equals `c` cost nothing.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                      | Variables                               |
| ---------------------------------------------------- | --------------------------------------- |
| `flips = 0`                                          | `flips = 0`                             |
| `x, y, z = (a >> i) & 1, (b >> i) & 1, (c >> i) & 1` | `flips = 1, i = 1, x = 1, y = 1, z = 0` |
| `for i in range(31):`                                | `flips = 3, i = 4, x = 0, y = 0`        |
| `for i in range(31):`                                | `i = 9`                                 |
| `for i in range(31):`                                | `i = 15`                                |
| `for i in range(31):`                                | `i = 20`                                |
| `for i in range(31):`                                | `i = 26`                                |
| `return`                                             | `returned = 3`                          |

### Complexity

- Time: O(1) time, 31 bits constant.
- Extra space: O(1) extra space.
- The brute force takes O(2^12) 12 bits enumerated.
