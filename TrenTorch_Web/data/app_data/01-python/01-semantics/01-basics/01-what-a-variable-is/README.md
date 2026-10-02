---
name: python-what-a-variable-is
title: What a Variable Is
tags: [python-core, variables]
difficulty: Beginner
---

## Statement

Implement functions that declare, assign, and reassign variables, establishing the basic syntax and rules before anything about how Python stores values internally is introduced.

## Theory

A variable is a name you choose, used to hold a value so you can refer to it again later instead of retyping it. You create one by writing its name, an `=` sign, and the value it should hold:

```python
age = 25
```

`age` now holds the value `25`. Anywhere after this line, writing `age` refers to that value.

```python
age = 25
print(age)          # 25
print(age + 5)       # 30
```

**Naming rules.** A variable name:

- Can contain letters, digits, and underscores.
- Cannot start with a digit.
- Cannot be a reserved word Python already uses for something else (like `if`, `for`, `def`, `return`).
- Is case-sensitive — `age` and `Age` are two completely different variables.

By convention, Python variable names use lowercase words separated by underscores, e.g. `total_score`, not `TotalScore` or `totalScore`. This is a style convention, not a rule the language enforces, but it's the near-universal standard in Python code.

**Reassigning a variable** simply means using `=` again with the same name. The variable now holds the new value; the old value is no longer reachable through that name.

```python
age = 25
age = 26     # age now holds 26
```

A single line can also update a variable based on its current value:

```python
age = 25
age = age + 1     # reads the current value (25), adds 1, stores 26
```

This exact pattern — read the current value, compute something from it, store the result back — is so common that Python provides shorthand operators for it:

```python
age += 1     # equivalent to age = age + 1
age -= 1     # equivalent to age = age - 1
age *= 2     # equivalent to age = age * 2
```

**Multiple variables** can be assigned in one line:

```python
x, y = 10, 20
```

This assigns `10` to `x` and `20` to `y` in a single statement.

A variable can hold any kind of value — a number, text (a string, written in quotes), or, as later topics cover, more complex kinds of data entirely. What a variable actually _is_ underneath this syntax — and why that matters — is covered in the next topic, once the idea of an "object" has been introduced.

## Explanation

`compute_total` is a direct translation of the four numbered steps: multiply, compute 8% of that, then fold the tax back in with `+=` rather than a fresh assignment, so the exercise actually exercises the shorthand-operator form the theory introduces rather than sidestepping it with `subtotal = subtotal + tax`. `swap_two_variables` uses a third variable rather than tuple-unpacking (`a, b = b, a`) on purpose — that shorthand is introduced later, and doing the swap by hand here is what makes "a variable is just a name pointing at a value" concrete before any syntactic sugar hides the steps.
