---
name: sheet-backspace-string-compare
title: 'Backspace String Compare'
tags: [dsa-sheet, stack-and-queue, stack-basics]
difficulty: Beginner
---

## Statement

`s` and `t` are typed into empty text editors. A `#` means **backspace** (it deletes the character before it; if the text is empty it does nothing). Return `True` if the two texts are **equal** after all the typing.

For `s = "ab#c"` and `t = "ad#c"` both become `"ac"`.

### Examples

**Example 1**

Input:

```python
backspace_compare('ab#c', 'ad#c')
```

Output:

```text
True
```

**Explanation:** Processing ab#c yields a b then backspace removes b then c gives ac. Processing ad#c yields a d then backspace removes d then c gives ac. The two results are equal so the function returns true.

**Example 2**

Input:

```python
backspace_compare('a#c', 'b')
```

Output:

```text
False
```

**Explanation:** Processing a#c removes a with backspace leaving empty then adds c giving c. Processing b adds b giving b. The results c and b differ so the function returns false.

### Constraints

- `0 <= len(s), len(t) <= 200000`
- Letters `a` to `z` and `#`.

## Theory

A text editor is a stack: a letter is pushed and a backspace pops (unless the stack is empty). Build the final text of each string with this rule and compare them.

There is a trick with `O(1)` memory: scan both strings **from the end**, skipping characters that a backspace erases, and compare what is left, but the stack version is the clear first step.

## Explanation

The helper `typed` applies the keys to a list and returns the text; `#` pops only when the list is not empty.

### Complexity

- Time: O(n + m) where n and m are lengths of s and t.
- Extra space: O(n + m) for the two lists.
- The brute force takes O(n^2 + m^2) where n and m are lengths of s and t.
