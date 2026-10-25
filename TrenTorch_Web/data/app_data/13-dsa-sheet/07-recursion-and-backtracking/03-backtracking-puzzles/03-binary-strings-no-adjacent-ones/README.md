---
name: sheet-binary-strings-no-adjacent-ones
title: 'Binary Strings Without Two Ones in a Row'
tags: [dsa-sheet, recursion, backtracking-puzzles]
difficulty: Beginner
---

## Statement

Return every **binary string of length `n`** (made of `0` and `1`) that does **not** contain two `1`s next to each other, in dictionary order. For `n = 3`: `000, 001, 010, 100, 101`. For `n = 0` the answer is the single empty string `[""]`.

### Examples

**Example 1**

Input:

```python
no_adjacent_ones(3)
```

Output:

```text
['000', '001', '010', '100', '101']
```

**Explanation:** The recursion first appends 0, then conditionally appends 1 if the previous character is not 1, generating exactly the five strings of length 3 with no adjacent 1s in dictionary order.

**Example 2**

Input:

```python
no_adjacent_ones(0)
```

Output:

```text
['']
```

**Explanation:** When n is 0 the base case triggers immediately, adding the empty string to the result.

### Constraints

- `0 <= n <= 16`
- The answer has about `1.6^n` strings (4,181 for `n = 18`).

## Theory

Build the string one character at a time, always **keeping it valid**. A `0` can always be added. A `1` can be added only if the previous character was **not** a `1`. Trying `0` first gives dictionary order.

Because the rule is checked while building, every branch of the recursion can be completed into a valid string, so nothing is wasted. The count of valid strings follows the **Fibonacci** numbers: a valid string of length `n` ends in `0` (any valid string of length `n - 1` before it) or in `01` (any valid string of length `n - 2` before it), so `count(n) = count(n - 1) + count(n - 2)`.

## Explanation

`go(prefix)` returns when the prefix has length `n`. It always tries adding `0`, and tries adding `1` only when the prefix is empty or does not end in `1`.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line   | Variables                                                           |
| ----------------- | ------------------------------------------------------------------- |
| `out = []`        | `out = []`                                                          |
| `def go(prefix):` | `go = <function no_adjacent_ones.<locals>.go at 0x000001F485501...` |
| `go("")`          | `out = ['000', '001', '010', '100', '101']`                         |
| `return`          | `returned = ['000', '001', '010', '100', '101']`                    |

### Complexity

- Time: O(2^n) where n is the input length.
- Extra space: O(n) recursion depth where n is the input length.
- The brute force takes O(n * 2^n) where n is the input length.
