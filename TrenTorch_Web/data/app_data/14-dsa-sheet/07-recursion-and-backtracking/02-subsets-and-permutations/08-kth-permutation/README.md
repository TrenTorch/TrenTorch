---
name: sheet-kth-permutation
title: 'The Kth Permutation'
tags: [dsa-sheet, recursion, subsets-and-permutations]
difficulty: Advanced
theory: jumping-straight-to-the-kth-permutation
---

## Statement

The numbers `1, 2, ..., n` have `n!` orderings. List them in dictionary order (`"123", "132", "213", "231", "312", "321"` for `n = 3`). Return the **`k`-th** one (counting from `1`) as a string of digits, for example `"213"`. For `n` above 9 the digits can be bigger than 9, so write the numbers one after another as in `"12345678910111213"`.

Generating all orderings first is impossible for large `n`: find the answer directly.

### Examples

**Example 1**

Input:

```python
kth_permutation(3, 3)
```

Output:

```text
'213'
```

The third ordering of 1, 2, 3 is `213`.

**Example 2**

Input:

```python
kth_permutation(4, 9)
```

Output:

```text
'2314'
```

The ninth ordering of 1, 2, 3, 4 is `2314`.

### Constraints

- `1 <= n <= 18`
- `1 <= k <= n!`

## Explanation

`k -= 1` turns it into a zero-based index. For each position, `divmod(k, factorial)` gives the index of the number to take from the remaining list and the leftover position inside the block. The chosen number is popped and the factorial shrinks.

### Complexity

- Time: O(n^2). For each of the `n` positions one `divmod` and one `pop` from a list of up to `n` values.
- Space: O(n). The list of unused numbers and the output.
