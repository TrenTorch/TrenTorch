---
name: sheet-simplify-path
title: 'Simplify a File Path'
tags: [dsa-sheet, stack-and-queue, stack-basics]
difficulty: Intermediate
---

## Statement

`path` is an absolute Unix-style path. Return its **canonical form**:

- it starts with a single `/`,
- names are separated by exactly one `/`,
- there is no trailing `/` (except for the root `/` itself),
- `.` (this directory) is removed, and `..` (parent directory) removes the previous name (at the root it does nothing).

For `"/a/./b/../../c/"` the answer is `"/c"`.

### Examples

**Example 1**

Input:

```python
simplify_path('/home/')
```

Output:

```text
'/home'
```

**Example 2**

Input:

```python
simplify_path('/a/./b/../../c/')
```

Output:

```text
'/c'
```

### Constraints

- `1 <= len(path) <= 100000`
- Letters, digits, `.`, `_` and `/`; `path` starts with `/`.
- A name made only of three or more dots, like `...`, is an ordinary name.

## Theory

A **stack** is last in, first out: you only add (`push`) and remove (`pop`) at the top. In Python a list does this with `append()` and `pop()`, both `O(1)`.

Split the path on `/` to get the names. Then handle each name: an empty name or `.` means nothing, `..` goes to the parent (**pop** the stack if it is not empty), and any other name goes one level deeper (**push**). The stack is the current directory path.

Finally join the stack with `/` and put a `/` in front. An empty stack gives `/`. A stack is the right tool because `..` undoes the **latest** step.

## Explanation

`path.split("/")` gives empty strings for repeated slashes; they are skipped like `.`. A `..` at the root pops nothing.
