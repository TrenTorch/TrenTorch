---
name: sheet-josephus
title: 'The Josephus Problem'
tags: [dsa-sheet, recursion, recursive-thinking]
difficulty: Advanced
---

## Statement

`n` people stand in a circle, numbered `1` to `n`. Starting at person `1`, count `k` people (counting person `1` as the first) and remove the person you land on; then start counting again from the next person still in the circle. Continue until one person is left. Return the **number** of the survivor.

For `n = 5` and `k = 2`: people `2`, `4`, `1`, `5` are removed in turn and person `3` survives.

The starter code simulates the circle by removing people from a list. It is correct but too slow for large `n` and `k`. Make it fast.

### Examples

**Example 1**

Input:

```python
josephus(5, 2)
```

Output:

```text
3
```

**Explanation:** With 5 people and step 2, eliminations are 2, 4, 1, 5 leaving person 3.

**Example 2**

Input:

```python
josephus(1, 7)
```

Output:

```text
1
```

**Explanation:** With only one person, no elimination occurs, so person 1 survives.

### Constraints

- `1 <= n <= 2 * 10**5`
- `1 <= k <= 10**9`

## Theory

Simulating every removal costs `O(n)` per removal when you delete from the middle of a list, `O(n²)` overall. There is a recurrence that needs no simulation.

Let `J(m)` be the survivor's **position (counting from 0)** in a circle of `m` people. With one person the survivor is position `0`. After the first removal the circle has `m - 1` people, but counting restarts `k` places further along. A position `p` in the smaller circle corresponds to position `(p + k) % m` in the bigger circle. So `J(m) = (J(m - 1) + k) % m`.

Compute it with a loop from `m = 2` up to `n`: `O(n)` time and `O(1)` memory. Add `1` at the end to count from 1. It is a fine example of **thinking recursively but computing iteratively**.

## Explanation

`position` starts at `0` (one person, counting from 0). For every circle size `m` from 2 to `n`, `position = (position + k) % m`. The survivor is `position + 1` when numbering from 1.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                 | Variables             |
| ------------------------------- | --------------------- |
| `position = 0`                  | `position = 0`        |
| `for m in range(2, n + 1):`     | `m = 2`               |
| `for m in range(2, n + 1):`     | `m = 3`               |
| `position = (position + k) % m` | `position = 2`        |
| `position = (position + k) % m` | `position = 0, m = 4` |
| `for m in range(2, n + 1):`     | `m = 5`               |
| `position = (position + k) % m` | `position = 2`        |
| `return`                        | `returned = 3`        |

### Complexity

- Time: O(n) time, n is the number of people.
- Extra space: O(1) extra memory.
- The brute force takes O(n^2) time, n is the number of people.
