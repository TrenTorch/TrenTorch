---
name: agentic-validate-tool-arguments
title: Argument Schema Validation
tags: [agentic-systems, tools, validation, json-schema]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Every tool advertises a **schema** describing its arguments: which are required, what type each has, which values are allowed. The model reads the schema when deciding how to call the tool, but nothing forces it to comply, so the executor must validate the arguments before running anything with side effects. A small subset of JSON Schema covers most tools: a type for each property (`string`, `integer`, `number`, `boolean`, `array`), an optional list of allowed values (`enum`) and optional `minimum` and `maximum` for numbers. The error messages are part of the contract because they are fed back to the model so that it can fix its call.

### From theory to code

Implement `validate_arguments`.

### Constraints

- `schema` has `properties` (name to spec with `type` and optional `enum`, `minimum`, `maximum`) and `required` (list of names). Return a sorted list of error strings, empty when valid.
- Errors: `missing: {name}` for each required name absent from `args`; `unexpected: {name}` for each argument not in `properties`; `type: {name}` when the value has the wrong type; `enum: {name}` when the value is not in `enum`; `range: {name}` when a number is below `minimum` or above `maximum`.
- Type rules: `integer` accepts `int` but **not** `bool`; `number` accepts `int` or `float` but not `bool`; `string`, `boolean` and `array` accept `str`, `bool` and `list` respectively.
- Check `enum` and `range` only if the type is correct. Report at most one of `type`, `enum`, `range` per argument.

### Hints

<details>
<summary>Hint 1</summary>

`isinstance(True, int)` is `True` in Python, so test for `bool` first.

</details>

<details>
<summary>Hint 2</summary>

Return `sorted(errors)` so the result does not depend on iteration order.

</details>

## Theory

### The simple version

A customs officer checks a form: every mandatory box filled, nothing written outside the boxes, numbers in the number boxes and values from the allowed list.

### The formula

$$
\text{valid}(a) \iff \text{req} \subseteq \text{keys}(a) \subseteq \text{props} \;\wedge\; \forall k:\; \text{type}(a_k) = \tau_k \wedge a_k \in \text{enum}_k \wedge m_k \le a_k \le M_k
$$

### How this is done in practice

The `jsonschema` library implements the full standard, and Pydantic validates the same constraints from Python types. Strict mode in function-calling APIs asks the provider to enforce the schema during generation, but executor-side validation remains necessary for security.

## Explanation

One pass over the arguments with type-guarded checks. The bool-versus-int trap is the classic bug in hand-written validators and is tested explicitly.
