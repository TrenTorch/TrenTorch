---
name: sheet-restore-ip-addresses
title: 'Restore IP Addresses'
tags: [dsa-sheet, recursion, backtracking-puzzles]
difficulty: Intermediate
---

## Statement

`s` is a string of digits. Return every **valid IP address** you can make by inserting three dots into `s` (without removing or reordering digits), sorted as strings. A valid address has **four parts**, each a number from `0` to `255` with **no leading zero** (the single digit `"0"` is fine, `"01"` is not).

For `"25525511135"`: `255.255.11.135` and `255.255.111.35`.

### Examples

**Example 1**

Input:

```python
restore_ip_addresses('25525511135')
```

Output:

```text
['255.255.11.135', '255.255.111.35']
```

**Example 2**

Input:

```python
restore_ip_addresses('0000')
```

Output:

```text
['0.0.0.0']
```

### Constraints

- `0 <= len(s) <= 14`
- `s` contains only digits.

## Theory

Choose **how long each of the four parts is**: 1, 2 or 3 digits. That is a recursion of depth four with three choices each, at most 81 possibilities, so it is tiny.

`go(start, parts)`: if you have four parts, the string must be fully used, and then you have an answer. Otherwise try the next part as `s[start:start + length]` for length 1, 2 or 3, and **prune** when the part is invalid (it has a leading zero, or its value is over `255`) or when the remaining digits cannot fill the remaining parts (each part takes at most 3 digits and at least 1).

The validity rules (range and leading zeros) are the whole difficulty; the recursion is simple.

## Explanation

With four parts the whole string must be used (`start == len(s)`). For fewer parts, every length from 1 to 3 is tried; a part is valid when it does not start with `0` (unless it is exactly `"0"`) and is at most `255`. The final list is sorted.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line         | Variables                                                              |
| ----------------------- | ---------------------------------------------------------------------- |
| `out = []`              | `out = []`                                                             |
| `def valid(part):`      | `valid = <function restore_ip_addresses.<locals>.valid at 0x000001...` |
| `def go(start, parts):` | `go = <function restore_ip_addresses.<locals>.go at 0x000001F48...`    |
| `go(0, [])`             | `out = ['255.255.11.135', '255.255.111.35']`                           |
| `return`                | `returned = ['255.255.11.135', '255.255.111.35']`                      |

### Complexity

- Time: O(1) fixed depth four, three branches per level.
- Extra space: O(1) auxiliary space for recursion depth four.
- The brute force takes O(n^3) n is length of s.
