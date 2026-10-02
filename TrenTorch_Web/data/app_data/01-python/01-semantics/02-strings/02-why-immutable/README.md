---
name: python-strings-why-immutable
title: Why Strings Are Immutable
tags: [python-strings, mutation]
difficulty: Beginner
---

## Statement

Implement functions that produce a "modified" version of a string, making explicit that every such operation builds a new string object and leaves the original untouched.

## Theory

`str` is an immutable type: the object at a given address can never be changed after it is created. Trying to assign into a string directly raises `TypeError`:

```python
s = "hello"
s[0] = "J"      # TypeError: 'str' object does not support item assignment
```

Every operation that appears to modify a string builds a **new string object** and returns it. The original is left exactly as it was; the variable only changes if you reassign it to the result.

Two consequences follow:

1. **Aliases are always safe.** If `y = s`, both variables store the same address. Because the object can never change, nothing done through `s` can alter what `y` sees.
2. **String methods never modify their receiver.** `s.upper()` returns a new string; writing it alone, without storing the result, has no lasting effect.

To "change one character," build the result from pieces: everything before the position, the new text, and everything after it — using slices from the previous topic.

**Where this matters later.** Immutability is why strings can be dictionary keys and set members. The same "returns a new object" pattern reappears in NumPy, where many operations return new arrays and only some modify in place.

## Explanation

`replace_char_at` builds the result as `s[:index] + ch + s[index+1:]` after normalizing a negative `index` to its positive equivalent — three pieces around the target position, exactly the "everything before, the new text, everything after" pattern the theory describes. `insert_at` skips manual index normalization entirely and relies on Python's own slice clamping: `s[:index] + text + s[index:]` naturally appends when `index` is past the end and clamps to the start when it's more negative than `-len(s)`, since a Python slice never raises for an out-of-range bound.
