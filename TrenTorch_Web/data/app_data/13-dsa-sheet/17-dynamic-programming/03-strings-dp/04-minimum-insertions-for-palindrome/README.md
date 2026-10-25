---
name: sheet-minimum-insertions-for-palindrome
title: 'Insertions to Make a Palindrome'
tags: [dsa-sheet, dynamic-programming, strings-dp]
difficulty: Intermediate
---

## Statement

You may insert characters **anywhere** in `s`. Return the **fewest insertions** needed to make `s` a palindrome.

For `"mbadm"` the answer is `2` (`"mbdadbm"`); for `"leetcode"` it is `5`.

### Examples

**Example 1**

Input:

```python
min_insertions('mbadm')
```

Output:

```text
2
```

**Explanation:** "mbadm" requires 2 insertions to match reversed 'mbadm', forming 'mbdadbm' which is palindrome.

**Example 2**

Input:

```python
min_insertions('leetcode')
```

Output:

```text
5
```

**Explanation:** "leetcode" needs 5 insertions; adding letters creates mirrored string with minimal additions.

### Constraints

- `0 <= len(s) <= 1000`
- Lower-case letters.

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

The characters that **already form a palindromic subsequence** can stay as they are; every other character needs a mirror image inserted next to the right place. So the answer is `len(s) - (length of the longest palindromic subsequence)`.

This is a good example of **reducing** a question to one you solved: compute the longest palindromic subsequence with the interval DP and subtract it from the length. `O(n²)`.

## Explanation

The helper is the longest palindromic subsequence table from the previous question. Characters outside it each cost one insertion.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                     | Variables                                                     |
| ----------------------------------- | ------------------------------------------------------------- |
| `n = len(s)`                        | `n = 5`                                                       |
| `for i in range(n - 1, -1, -1):`    | `prev = [0, 0, 0, 0, 1], i = 3, cur = [0, 0, 0, 0, 1]`        |
| `for i in range(n - 1, -1, -1):`    | `prev = [0, 0, 0, 1, 1], i = 2, cur = [0, 0, 0, 1, 1], j = 4` |
| `cur[j] = max(prev[j], cur[j - 1])` | `cur = [0, 0, 1, 1, 1]`                                       |
| `cur[j] = max(prev[j], cur[j - 1])` | `prev = [0, 0, 1, 1, 1], i = 1, cur = [0, 1, 1, 0, 0], j = 2` |
| `for i in range(n - 1, -1, -1):`    | `prev = [0, 1, 1, 1, 1], i = 0, cur = [0, 1, 1, 1, 1], j = 4` |
| `cur[j] = max(prev[j], cur[j - 1])` | `cur = [1, 1, 1, 0, 0], j = 2`                                |
| `return`                            | `returned = 2`                                                |

### Complexity

- Time: O(n^2) time, n equals string length.
- Extra space: O(n) additional memory, n is length of s.
- The brute force takes O(2^n) time, n equals string length.
