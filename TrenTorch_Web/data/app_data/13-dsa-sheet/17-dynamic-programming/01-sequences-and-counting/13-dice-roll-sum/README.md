---
name: sheet-dice-roll-sum
title: 'Dice Roll Sum'
tags: [dsa-sheet, dynamic-programming, sequences-and-counting]
difficulty: Intermediate
---

## Statement

You roll `dice` dice, each with faces numbered `1` to `faces`. Return the **number of ways** (different sequences of results) that the faces **add up to `target`**. Return the answer modulo `10**9 + 7`.

For `dice = 2`, `faces = 6` and `target = 7` the answer is `6`.

The starter code tries every face for every die. It is correct but too slow for many dice.

### Examples

**Example 1**

Input:

```python
dice_ways(2, 6, 7)
```

Output:

```text
6
```

**Explanation:** Two six-sided dice add up to 7 in 6 ways: 1+6, 2+5, 3+4, 4+3, 5+2 and 6+1.

**Example 2**

Input:

```python
dice_ways(1, 2, 3)
```

Output:

```text
0
```

**Explanation:** One die with 2 faces gives at most 2, so a sum of 3 is impossible: 0 ways.

### Constraints

- `0 <= dice <= 100`
- `1 <= faces <= 60`
- `0 <= target <= 1000`

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

**State:** `ways(d, t)`, the number of ways `d` dice can sum to `t`. **Transition:** the last die shows a face `f`, so `ways(d, t) = sum of ways(d - 1, t - f)` for `f = 1..faces`. **Base case:** `ways(0, 0) = 1`.

Keep one row per number of dice. The sum over `faces` terms can be made `O(1)` with a **sliding window** (or prefix sums): each new total is the previous window sum plus one entering value minus one leaving value. Then the whole thing is `O(dice × target)`.

## Explanation

`row[t]` is the number of ways for the current number of dice. `prefix` makes each window sum a subtraction of two prefix values.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                          | Variables                                                                                                            |
| -------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `mod = 10**9 + 7`                                        | `mod = 1000000007`                                                                                                   |
| `for t in range(target + 1):`                            | `row = [1, 0, 0, 0, 0, 0, 0, 0], _ = 0, prefix = [0, 1, 1, 1, 0, 0, 0, 0, 0], t = 3`                                 |
| `prefix[t + 1] = (prefix[t] + row[t]) % mod`             | `prefix = [0, 1, 1, 1, 1, 1, 1, 1, 1], t = 7`                                                                        |
| `for t in range(1, target + 1):`                         | `t = 5, nxt = [0, 1, 1, 1, 1, 0, 0, 0]`                                                                              |
| `for t in range(target + 1):`                            | `row = [0, 1, 1, 1, 1, 1, 1, 0], _ = 1, prefix = [0, 0, 0, 0, 0, 0, 0, 0, 0], t = 1, nxt = [0, 1, 1, 1, 1, 1, 1, 0]` |
| `for t in range(target + 1):`                            | `prefix = [0, 0, 1, 2, 3, 4, 5, 0, 0], t = 6`                                                                        |
| `nxt[t] = (prefix[t] - prefix[max(0, t - faces)]) % mod` | `prefix = [0, 0, 1, 2, 3, 4, 5, 6, 6], t = 3, nxt = [0, 0, 1, 2, 0, 0, 0, 0]`                                        |
| `return`                                                 | `returned = 6`                                                                                                       |

### Complexity

- Time: O(dice * target).
- Extra space: O(target).
- The brute force takes O(faces^dice).
