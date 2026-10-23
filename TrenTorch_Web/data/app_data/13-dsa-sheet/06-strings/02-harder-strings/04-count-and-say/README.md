---
name: sheet-count-and-say
title: 'Count and Say'
tags: [dsa-sheet, strings, harder-strings]
difficulty: Intermediate
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

## Theory

Each term is built from the previous one, so loop `n - 1` times, each time **run-length encoding** the current string: scan for runs of equal digits and write `count` followed by `digit` for each run.

`itertools.groupby(term)` yields each run, so one step is `"".join(str(len(list(run))) + digit for digit, run in groupby(term))`. The strings grow by about 30% every step, which is why `n` is limited to 40.

A famous fact: no term ever contains a digit bigger than `3`, and the sequence grows by a constant ratio (Conway's constant, about 1.3036). It is an example of a **simulation**: no trick, just do what the rules say, carefully.

## Explanation

Start with `"1"` and apply the describe step `n - 1` times. `groupby` splits the string into runs; each run becomes its length followed by its digit.
