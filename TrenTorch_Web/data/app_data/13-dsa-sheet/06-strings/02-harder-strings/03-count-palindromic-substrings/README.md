---
name: sheet-count-palindromic-substrings
title: 'Count Palindromic Substrings'
tags: [dsa-sheet, strings, harder-strings]
difficulty: Intermediate
---

## Statement

Return how many **substrings** of `s` are palindromes. Substrings at different positions count separately, even if they hold the same characters (`"aaa"` has 6: three `a`, two `aa` and one `aaa`).

The starter code checks every substring. It is correct but too slow. Make it fast.

### Examples

**Example 1**

Input:

```python
count_palindromic_substrings('abc')
```

Output:

```text
3
```

**Explanation:** For "abc", each character is a palindrome, and no longer substring matches, hence 3.

Only the three single letters.

**Example 2**

Input:

```python
count_palindromic_substrings('aaa')
```

Output:

```text
6
```

**Explanation:** For "aaa", single letters count three, two-letter pairs count two, and the whole string counts one, totaling 6.

`a` three times, `aa` twice, `aaa` once: 6.

### Constraints

- `0 <= len(s) <= 1000`
- `s` contains lower-case letters.

## Theory

The same **expand around the centre** idea counts palindromes without checking each substring from scratch. Every palindromic substring has exactly one centre, and if a substring around a centre is a palindrome, so is every smaller one around the same centre. So when you expand from a centre and the characters match `k` times, you have found exactly `k` palindromes.

Count one for every successful step of the expansion, over all `2n - 1` centres. The worst case (a string of one repeated letter) is `O(n²)`, which is also the number of palindromes it has.

## Explanation

For each centre, `left` and `right` start at the centre (equal for odd lengths, adjacent for even lengths). Each time `s[left] == s[right]` a new palindrome has been found: add one and widen. The total over all centres is the answer.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line      | Variables                         |
| -------------------- | --------------------------------- |
| `n = len(s)`         | `n = 3`                           |
| `left = center // 2` | `count = 0, center = 0, left = 0` |
| `left -= 1`          | `count = 1, left = -1, right = 0` |
| `left = center // 2` | `center = 1, left = 0, right = 1` |
| `left -= 1`          | `count = 2, center = 2`           |
| `left = center // 2` | `center = 3, left = 1, right = 2` |
| `count += 1`         | `count = 3, center = 4, left = 2` |
| `return`             | `returned = 3`                    |

### Complexity

- Time: O(n^2), n length.
- Extra space: O(1), constant.
- The brute force takes O(n^3), n length.
