---
name: sheet-palindrome-partitioning-ii
title: 'Palindrome Partitioning: Fewest Cuts'
tags: [dsa-sheet, dynamic-programming, intervals-and-states]
difficulty: Advanced
theory: palindrome-partitioning
---

## Statement

Return the **fewest cuts** needed to split `s` into pieces that are all **palindromes**. A string that is already a palindrome needs `0` cuts.

For `"aab"` the answer is `1` (`"aa" | "b"`).

The starter code re-checks pieces and repeats work. It is correct but too slow for long strings.

### Examples

**Example 1**

Input:

```python
min_cut_palindromes('aab')
```

Output:

```text
1
```

**Example 2**

Input:

```python
min_cut_palindromes('ab')
```

Output:

```text
1
```

### Constraints

- `0 <= len(s) <= 1000`
- Lower-case letters.

## Explanation

`cuts[i]` is the fewest cuts for the first `i` letters, starting from the worst case `i - 1` (cut between every letter) and `cuts[0] = -1`. Instead of a table of which substrings are palindromes, grow every palindrome around its centre (odd and even). Each palindrome `s[l..r]` that is found says: the first `r + 1` letters can be done with `cuts[l] + 1` cuts. Centres are processed from left to right, so `cuts[l]` is already final when it is used.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                                | Variables                                               |
| -------------------------------------------------------------- | ------------------------------------------------------- |
| `n = len(s)`                                                   | `n = 3`                                                 |
| `for left, right in ((centre, centre), (centre, centre + 1)):` | `cuts = [-1, 0, 1, 2], centre = 0, left = 0, right = 0` |
| `for left, right in ((centre, centre), (centre, centre + 1)):` | `right = 1`                                             |
| `right += 1`                                                   | `cuts = [-1, 0, 0, 2], left = -1, right = 2`            |
| `left -= 1`                                                    | `centre = 1, left = 0, right = 1`                       |
| `for centre in range(n):`                                      | `centre = 2, left = 1, right = 2`                       |
| `left -= 1`                                                    | `cuts = [-1, 0, 0, 1]`                                  |
| `return`                                                       | `returned = 1`                                          |

### Complexity

- Time: O(n^2). Every palindromic substring is found by growing around its centre, and each one updates a single cell.
- Space: O(n). One array of cuts.
