---
name: python-strings-immutability
title: 'Immutability & Concatenation'
tags: [python-strings, mutation, performance]
difficulty: Intermediate
---

## Statement

Implement functions that produce a "modified" version of a string while leaving the original untouched, build strings with `+`, `+=` and `*` and model how much copying repeated concatenation performs.

## Theory

### Why strings are immutable

`str` is an immutable type: the object at a given address can never be changed after it is created. Trying to assign into a string directly raises `TypeError`:

```python
s = "hello"
s[0] = "J"      # TypeError: 'str' object does not support item assignment
```

Every operation that appears to modify a string builds a **new string object** and returns it. The original is left exactly as it was; the variable only changes if you reassign it to the result.

Two consequences follow:

1. **Aliases are always safe.** If `y = s`, both variables store the same address. Because the object can never change, nothing done through `s` can alter what `y` sees.
2. **String methods never modify their receiver.** `s.upper()` returns a new string; writing it alone, without storing the result, has no lasting effect.

To "change one character," build the result from pieces: everything before the position, the new text, and everything after it, using slices.

**Where this matters later.** Immutability is why strings can be dictionary keys and set members. The same "returns a new object" pattern reappears in NumPy, where many operations return new arrays and only some modify in place.

### Concatenation & its cost

`+` on two strings builds a **new string** containing the characters of the left operand followed by the right. `*` with an `int` repeats a string; zero or negative counts give an empty string.

`s += t` is shorthand for `s = s + t`. Because strings are immutable, this is not mutation, it creates a new string and reassigns `s` to store the new address.

```python
result = ""
for word in ["a", "b", "c"]:
    result += word
```

Each pass through that loop builds a brand-new string holding everything in `result` plus `word`, then reassigns `result` to it.

**The cost.** Producing a new string of length $L$ requires writing $L$ characters. If you append $n$ pieces, each of length $p$, one at a time, the total number of characters written across every step is:

$$\sum_{k=1}^{n} k \cdot p \;=\; p \cdot \frac{n(n+1)}{2}$$

This grows with the **square** of $n$: ten times as many pieces means roughly a hundred times as much copying. CPython contains an optimization that sometimes resizes a string in place when nothing else refers to it, but the language does not guarantee this, code should not depend on it.

**Where this matters later.** The same pattern, repeated "append by making a new object", appears when arrays are grown one element at a time inside loops. Building results in one step instead of reallocating on every iteration carries directly into NumPy and PyTorch code.

## Explanation

`replace_char_at` builds the result as `s[:index] + ch + s[index+1:]` after normalizing a negative `index` to its positive equivalent, three pieces around the target position, exactly the "everything before, the new text, everything after" pattern the theory describes. `insert_at` skips manual index normalization entirely and relies on Python's own slice clamping: `s[:index] + text + s[index:]` naturally appends when `index` is past the end and clamps to the start when it's more negative than `-len(s)`, since a Python slice never raises for an out-of-range bound.

`join_with_separator` is written with a plain `for` loop and `+=` (per the exercise's own constraint of not using `join()`) tracking whether the separator has been emitted yet, rather than building it and stripping a trailing separator afterward, that avoids ever producing a string containing a separator that shouldn't be there in the first place. `total_chars_copied` is the closed-form formula itself (`piece_length * n * (n + 1) // 2`), not a simulated loop that actually performs `n` additions, a real loop would defeat the point of a formula that's supposed to answer "how much work would this take" in O(1).
