---
name: sheet-count-and-say
title: 'Count and Say'
tags: [dsa-sheet, strings, harder-strings]
difficulty: Intermediate
theory: reading-a-string-aloud
---

## Statement

The **count-and-say** sequence is a list of strings of digits. Term 1 is `"1"`. Each next term describes the previous one by reading its **runs** of equal digits aloud: how many, then which digit.

- Term 1: `"1"`
- Term 2: one `1`, so `"11"`
- Term 3: two `1`s, so `"21"`
- Term 4: one `2`, one `1`, so `"1211"`
- Term 5: one `1`, one `2`, two `1`s, so `"111221"`

Return term `n`.

### Examples

**Example 1**

Input:

```python
count_and_say(4)
```

Output:

```text
'1211'
```

**Example 2**

Input:

```python
count_and_say(1)
```

Output:

```text
'1'
```

### Constraints

- `1 <= n <= 40`
- Term 40 has about 63,000 digits.

## Explanation

Start with `"1"` and apply the describe step `n - 1` times. `groupby` splits the string into runs; each run becomes its length followed by its digit.

### Complexity

- Time: O(L). Each term is built in one pass over the previous term; the terms grow by a factor of about 1.3, so the total is a geometric series dominated by the last term of length `L`.
- Space: O(L). The current term and the next one.
