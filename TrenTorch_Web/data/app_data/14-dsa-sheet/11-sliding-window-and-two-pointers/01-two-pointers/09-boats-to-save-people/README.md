---
name: sheet-boats-to-save-people
title: 'Boats to Save People'
tags: [dsa-sheet, two-pointers, two-pointers]
difficulty: Intermediate
theory: pairing-the-heavy-with-the-light
---

## Statement

`people[i]` is the weight of person `i`. Each boat carries **at most two people** and a total weight of at most `limit`. Every person weighs at most `limit`. Return the **fewest boats** needed to carry everyone.

For `people = [3, 2, 2, 1]` and `limit = 3` the answer is `3` (`[1, 2]`, `[2]`, `[3]`).

### Examples

**Example 1**

Input:

```python
boats_needed([3, 2, 2, 1], 3)
```

Output:

```text
3
```

**Example 2**

Input:

```python
boats_needed([3, 5, 3, 4], 5)
```

Output:

```text
4
```

### Constraints

- `0 <= len(people) <= 200000`
- `1 <= people[i] <= limit <= 30000`

## Explanation

`heavy` always boards. `light` boards with them only if the sum fits; otherwise the heavy person leaves alone and `light` waits for the next, lighter, heavy person.

### Complexity

- Time: O(n log n). Sorting dominates; the two-pointer pairing is O(n).
- Space: O(n). The sorted copy.
