---
name: sheet-simplify-path
title: 'Simplify a File Path'
tags: [dsa-sheet, stack-and-queue, stack-basics]
difficulty: Intermediate
theory: walking-through-folders
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

## Explanation

`path.split("/")` gives empty strings for repeated slashes; they are skipped like `.`. A `..` at the root pops nothing.

### Complexity

- Time: O(n). One pass over the path parts.
- Space: O(n). The stack of directory names.
