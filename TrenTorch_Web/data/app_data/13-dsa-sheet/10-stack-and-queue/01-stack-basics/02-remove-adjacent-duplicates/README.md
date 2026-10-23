---
name: sheet-remove-adjacent-duplicates
title: 'Remove Adjacent Duplicates'
tags: [dsa-sheet, stack-and-queue, stack-basics]
difficulty: Beginner
---

## Statement

Repeatedly **delete two equal neighbouring characters** until none are left to delete, and return the remaining string. For `"abbaca"`: delete `bb` to get `"aaca"`, delete `aa` to get `"ca"`.

### Examples

**Example 1**

Input:

```python
remove_adjacent_duplicates('abbaca')
```

Output:

```text
'ca'
```

**Example 2**

Input:

```python
remove_adjacent_duplicates('azxxzy')
```

Output:

```text
'ay'
```

### Constraints

- `0 <= len(s) <= 200000`
- `s` contains lower-case letters.

## Theory

After a deletion, the two characters on both sides become neighbours, and may be equal too. That chain reaction is what a stack handles naturally. Keep the string built so far on a stack. For each new character: if it equals the top of the stack, **pop** (they cancel); otherwise **push**.

The stack always holds the answer for the part of the string read so far. `O(n)`.

## Explanation

The top of the stack is the last character that survived. A new character that matches it cancels it; otherwise it is kept.
