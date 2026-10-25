---
name: sheet-happy-number
title: 'Happy Number'
tags: [dsa-sheet, hashing, hashing-patterns]
difficulty: Beginner
---

## Statement

Replace `n` with the **sum of the squares of its digits**, and repeat. If you reach `1` the number is **happy**; if you instead loop forever in a cycle that never contains `1`, it is not. Return `True` for a happy number.

For example `19` is happy: `1² + 9² = 82`, `8² + 2² = 68`, `6² + 8² = 100`, `1² + 0² + 0² = 1`.

### Examples

**Example 1**

Input:

```python
happy_number(19)
```

Output:

```text
True
```

`19 -> 82 -> 68 -> 100 -> 1`.

**Example 2**

Input:

```python
happy_number(2)
```

Output:

```text
False
```

`2` falls into a cycle that never reaches 1.

### Constraints

- `1 <= n <= 2**31 - 1`

## Theory

The sequence either reaches `1` or enters a **cycle**. To detect a cycle, remember every value you have seen in a `set`: if a value comes up again, you are looping and the answer is `False`.

Why does the sequence not grow forever? A number with `d` digits has a digit-square sum of at most `81 * d`, which is far smaller than the number once `d` reaches 4. So after a few steps the values stay small, and with finitely many small values a repeat must happen.

A `set` of seen values detects cycles in `O(1)` per step. (Floyd's tortoise-and-hare detects cycles with `O(1)` memory; you will meet it for linked lists.)

## Explanation

`seen` holds every value visited. The loop keeps replacing `n` by the digit-square sum until it is `1` (return `True`) or already in `seen` (return `False`). `divmod(n, 10)` peels off the last digit.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line            | Variables                                               |
| -------------------------- | ------------------------------------------------------- |
| `seen = set()`             | `seen = set()`                                          |
| `total += digit * digit`   | `n = 1, seen = {19}, total = 81, digit = 9`             |
| `seen.add(n)`              | `n = 82, seen = {82, 19}, total = 82, digit = 1`        |
| `n, digit = divmod(n, 10)` | `n = 0, total = 4, digit = 8`                           |
| `n, digit = divmod(n, 10)` | `n = 6, seen = {82, 19, 68}, total = 0`                 |
| `n = total`                | `n = 100, total = 100, digit = 6`                       |
| `n, digit = divmod(n, 10)` | `n = 1, seen = {100, 82, 19, 68}, total = 0, digit = 0` |
| `return`                   | `returned = True`                                       |

### Complexity

- Time: O(log n) where n is the input number.
- Extra space: O(1) extra space.
- The brute force takes O(log n) where n is the input number.
