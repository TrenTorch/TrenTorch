---
name: sheet-add-two-numbers-lists
title: 'Add Two Numbers'
tags: [dsa-sheet, linked-list, linked-list-basics]
difficulty: Intermediate
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

## Theory

This is school addition. Start at the ones digits, which is also the **head** of each list, so the least significant digit comes first and a single pass does the whole job.

Keep a `carry`. In each round add the two current digits (a missing digit counts as 0) and the carry; the new node holds `total % 10` and the new carry is `total // 10`. Keep going while either list has nodes **or the carry is still 1** (so `99 + 1` produces the extra digit `100`).

You never need to turn the lists into big numbers: that would be wrong for 100,000 digits (and slow). Work digit by digit, with a dummy head to build the answer.

## Explanation

The loop condition includes `carry`, so a final carry becomes one more node. `a.val if a else 0` treats a shorter number as padded with zeros.
