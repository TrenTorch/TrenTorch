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

**Example 2**

Input:

```python
min_flips(4, 2, 7)
```

Output:

```text
1
```

### Constraints

- `0 <= a, b, c < 2**31`

## Theory

Positions are independent: look at each bit position `i` and the three bits `x`, `y` of `a`, `b` and `z` of `c`.

- If `z == 0`, both `x` and `y` must become `0`: you flip each one that is `1` (up to 2 flips).
- If `z == 1`, at least one of `x`, `y` must be `1`: if both are `0` you need 1 flip, otherwise 0.

Add up the flips over the 31 positions. The shortcut with masks: `needed = (a | b) ^ c` marks the positions where the OR is wrong. Where `c` is 0, the wrong positions cost `a_bit + b_bit` flips; where `c` is 1, they cost 1 flip.

## Explanation

The loop runs over bit positions and applies the case analysis above. Positions where `a | b` already equals `c` cost nothing.
