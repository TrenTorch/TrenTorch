---
name: python-strings-concatenation-cost
title: Concatenation and Its Cost
tags: [python-strings, performance]
difficulty: Intermediate
---

## Statement

Implement string building with `+`, `+=`, and `*`, and a function that models how much copying repeated concatenation performs.

## Theory

`+` on two strings builds a **new string** containing the characters of the left operand followed by the right. `*` with an `int` repeats a string; zero or negative counts give an empty string.

`s += t` is shorthand for `s = s + t`. Because strings are immutable, this is not mutation — it creates a new string and reassigns `s` to store the new address.

```python
result = ""
for word in ["a", "b", "c"]:
    result += word
```

Each pass through that loop builds a brand-new string holding everything in `result` plus `word`, then reassigns `result` to it.

**The cost.** Producing a new string of length $L$ requires writing $L$ characters. If you append $n$ pieces, each of length $p$, one at a time, the total number of characters written across every step is:

$$\sum_{k=1}^{n} k \cdot p \;=\; p \cdot \frac{n(n+1)}{2}$$

This grows with the **square** of $n$: ten times as many pieces means roughly a hundred times as much copying. CPython contains an optimization that sometimes resizes a string in place when nothing else refers to it, but the language does not guarantee this — code should not depend on it.

**Where this matters later.** The same pattern — repeated "append by making a new object" — appears when arrays are grown one element at a time inside loops. Building results in one step instead of reallocating on every iteration carries directly into NumPy and PyTorch code.

## Explanation

`join_with_separator` is written with a plain `for` loop and `+=` (per the exercise's own constraint of not using `join()`) tracking whether the separator has been emitted yet, rather than building it and stripping a trailing separator afterward — that avoids ever producing a string containing a separator that shouldn't be there in the first place. `total_chars_copied` is the closed-form formula itself (`piece_length * n * (n + 1) // 2`), not a simulated loop that actually performs `n` additions — a real loop would defeat the point of a formula that's supposed to answer "how much work would this take" in O(1).
