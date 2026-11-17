---
name: sheet-add-two-numbers-lists
title: 'Add Two Numbers'
tags: [dsa-sheet, linked-list, linked-list-basics]
difficulty: Intermediate
theory: adding-numbers-digit-by-digit
---

## Statement

Two non-negative whole numbers are stored as linked lists of digits in **reverse order**: the first node is the **ones** digit. So `2 -> 4 -> 3` is the number 342. Add the numbers and return the sum in the same format.

The tests show a list as a Python list of its values: `[1, 2, 3]` stands for `1 -> 2 -> 3`.

### Examples

**Example 1**

Input:

```python
add_two_numbers(l1, l2)  # l1 = 2 -> 4 -> 3 (342), l2 = 5 -> 6 -> 4 (465)
```

Output:

```text
[7, 0, 8]
```

**Example 2**

Input:

```python
add_two_numbers(l1, l2)  # l1 = 9 -> 9 -> 9 (999), l2 = 1
```

Output:

```text
[0, 0, 0, 1]
```

### Constraints

- `1 <= number of nodes <= 100000` in each list
- `0 <= val <= 9`
- No leading zeros (a last node of `0` appears only in the number 0 itself).

## Explanation

The loop condition includes `carry`, so a final carry becomes one more node. `a.val if a else 0` treats a shorter number as padded with zeros.

### Complexity

- Time: O(max(n, m)). One pass over both lists with a carry.
- Space: O(max(n, m)). The result list is new nodes (one per digit); no other memory is used.
