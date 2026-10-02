---
name: python-core-semantics-assemble
title: 'Assemble: Full Variable/Mutation Trace'
tags: [python-core, mutation, control-flow, loops]
difficulty: Advanced
---

## Statement

Implement a single function that combines every concept from this module — variables, functions, assignment, aliasing, mutation vs reassignment, mutable default arguments, conditionals, truthiness, and loops — into one realistic trace of a small data-processing task.

## Theory

This problem does not introduce new concepts. It requires combining every topic covered in this module into one function.

Specifically, this problem requires you to:

- Track object addresses (`id()`) to confirm exactly when mutation vs reassignment occurs, at each step.
- Use an alias (a second variable referring to the same list) and confirm what it does and doesn't observe.
- Use a default argument safely (avoiding the mutable default trap).
- Use truthy checks to control processing decisions per element.
- Use a `for` loop, with `continue` and `break` where appropriate, to process a collection.

There is no new theory beyond correctly combining the previous fifteen topics. Re-read any topic above if a specific behavior in the stub below is unclear before implementing.

## Explanation

`process_batch` mirrors the shape every earlier topic already established individually: a safe default (`seen=None`, per the Mutable Default Argument topic), a `for` loop with `continue` for the skip case and `break` for the stop case (per the loop topics), truthy-style zero detection rather than an explicit `== 0` (per the Truthy/Falsy topic — `if not number:` reads directly off the same falsy-zero rule), and mutating `seen` in place rather than reassigning it (per Reassignment vs Mutation), so that the alias created afterward genuinely observes the same object rather than a coincidentally-equal copy.
