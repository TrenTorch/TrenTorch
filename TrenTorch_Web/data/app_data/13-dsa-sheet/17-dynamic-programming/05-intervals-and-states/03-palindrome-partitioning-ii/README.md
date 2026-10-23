---
name: sheet-palindrome-partitioning-ii
title: 'Palindrome Partitioning: Fewest Cuts'
tags: [dsa-sheet, dynamic-programming, intervals-and-states]
difficulty: Advanced
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

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

Two tables work together. First, `pal[i][j]`, whether `s[i..j]` is a palindrome, filled by **expanding from the centre** or by `pal[i][j] = s[i] == s[j] and pal[i + 1][j - 1]`. Second, `cuts[j]`, the fewest cuts for the prefix `s[:j + 1]`: if the whole prefix is a palindrome it is `0`, else `cuts[j] = min(cuts[i - 1] + 1)` over `i` such that `s[i..j]` is a palindrome.

Both tables are `O(n²)`. Precomputing `pal` is what removes the repeated palindrome checks.

## Explanation

Expanding around each centre marks all palindromes; `cuts` then looks at every palindrome ending at `j`.
