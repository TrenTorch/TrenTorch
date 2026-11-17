---
name: sheet-happy-number
title: 'Happy Number'
tags: [dsa-sheet, hashing, hashing-patterns]
difficulty: Beginner
theory: detecting-a-loop
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

## Explanation

The digit-square sum is a function of the number, so repeating it either reaches `1` or enters a cycle, like a linked list that ends in a loop. Floyd's cycle detection needs no set: `slow` moves one step, `fast` moves two. If `fast` reaches `1` the number is happy; if the two meet first, the walk is in a cycle that does not contain `1`.

`step(x)` peels digits with `divmod(x, 10)` and adds their squares.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line           | Variables                                                            |
| ------------------------- | -------------------------------------------------------------------- |
| `def step(x):`            | `step = <function happy_number.<locals>.step at 0x000002BDE6FDC700>` |
| `slow, fast = n, step(n)` | `slow = 19, fast = 82`                                               |
| `slow = step(slow)`       | `slow = 82`                                                          |
| `fast = step(step(fast))` | `fast = 100`                                                         |
| `slow = step(slow)`       | `slow = 68`                                                          |
| `fast = step(step(fast))` | `fast = 1`                                                           |
| `return`                  | `returned = True`                                                    |

### Complexity

- Time: O(log n). The first step costs one pass over the digits; after that the value is below 1000, so the walk to `1` or into a cycle is a constant number of steps.
- Space: O(1). Floyd cycle detection keeps two numbers.
