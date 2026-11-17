---
name: agentic-argument-coercion
title: Argument Coercion & Defaults
tags: [agentic-systems, tools, validation, robustness]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Models are inconsistent about types. Asked for an integer they sometimes write `"3"`, for a boolean `"true"` or `"yes"`, for a number `"2.5"`. Rejecting every such call wastes a round trip with the model, while blindly accepting them risks silent bugs. A middle path is **coercion**: convert a value to the declared type when the conversion is unambiguous, leave it untouched when it is not (so validation can report it) and fill in **defaults** for optional arguments the model omitted. This is lenient where leniency is safe and strict everywhere else.

### From theory to code

Implement `coerce_arguments`.

### Constraints

- `schema` maps each argument name to a spec with `type` (`integer`, `number`, `boolean`, `string`) and an optional `default`. Return a new dict.
- For each argument present in `args`: a `str` value is coerced to `integer` with `int()`, to `number` with `float()`, and to `boolean` if its lowercase form is in `{'true', 'yes', '1'}` (True) or `{'false', 'no', '0'}` (False). Failed conversions leave the original value. Values already of the right type, and arguments not in `schema`, are copied unchanged.
- For each name in `schema` that is absent from `args` and has a `default`, add the default.
- A `float` such as `3.0` given for an `integer` is converted only when it is integral (`3.0 -> 3`); `3.5` is left unchanged. Do not modify `args`.

### Hints

<details>
<summary>Hint 1</summary>

Wrap the `int()` and `float()` calls in `try/except ValueError`.

</details>

<details>
<summary>Hint 2</summary>

Remember that `bool` is a subclass of `int`, so check for `bool` before `int` when deciding whether a value already has the right type.

</details>

## Theory

### The simple version

A forgiving shopkeeper accepts "three" and "3" for a quantity but asks again for "a few". Clear cases are accepted quietly, unclear ones are sent back.

### The formula

$$
\text{coerce}(v, \tau) = \begin{cases} \tau(v) & v \text{ is a string/number with an unambiguous reading as } \tau\\ v & \text{otherwise}\end{cases}
$$

### How this is done in practice

Pydantic's lax mode and many agent SDKs do this before validation. Anything coerced silently should be logged, because a pattern of coercions often reveals an unclear tool description that should be rewritten.

## Explanation

A small decision table per type, with the original value preserved on failure so that the validation step from the previous question can report it accurately.
