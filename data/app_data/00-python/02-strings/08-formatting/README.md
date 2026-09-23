---
name: python-strings-formatting
title: "Formatting: %, .format(), and f-strings"
tags: [python-strings, formatting]
difficulty: Intermediate
---

## Statement

Implement functions that produce exact, aligned text output using format specifications.

## Theory

Python has three ways to insert values into text: `%` formatting (older style), `.format()`, and f-strings (the primary style, a string literal prefixed with `f` that evaluates expressions inside `{}` at the moment the literal runs).

```python
who = "Ada"
age = 36
f"{who} is {age}"                       # "Ada is 36"
f"{age + 1}"                            # "37"     any expression is allowed
```

**Format specification.** After a colon inside the braces, a specification controls how the value is displayed: `{value:[fill][align][sign][0][width][,][.precision][type]}`.

| Part | Meaning | Example | Result |
|---|---|---|---|
| align `<` `>` `^` | left, right, center in the width | `f"{'ab':>5}"` | `"   ab"` |
| width | minimum total characters | `f"{7:3}"` | `"  7"` |
| `0` before width | zero padding for numbers | `f"{7:03}"` | `"007"` |
| `,` | thousands separator | `f"{1234567:,}"` | `"1,234,567"` |
| `.N` + `f` | N decimal places | `f"{3.14159:.2f}"` | `"3.14"` |
| `%` type | multiply by 100, add `%` | `f"{0.256:.1%}"` | `"25.6%"` |
| `b` | binary | `f"{5:b}"` | `"101"` |

**Extras.** `!r` inside the braces uses the `repr` form of a value, which shows quotes on strings: `f"{'Ada'!r}"` is `"'Ada'"`. A width or precision can itself come from a variable using nested braces: `f"{value:{width}.{prec}f}"`.

Text values are **truncated** only by an explicit precision — a width never shortens a value.

**Where this matters later.** Formatted output is how training loops print loss values and shapes (`f"loss={loss:.4f}"`). The `!r` form is a fast way to inspect variables while debugging.

## Explanation

`receipt_line` chains three format specs in one f-string (`f"{item:<12}{qty:>4}{price:>10.2f}"`) rather than building each field separately and concatenating, since the exact alignment/width contract is what the format spec itself guarantees — a width never truncates, so an over-long `item` naturally overflows past 12 characters instead of erroring. `format_percent`'s decimal count comes from a nested brace (`f"{value:.{decimals}%}"`), the mechanism the theory calls out for a precision that isn't a fixed literal.
