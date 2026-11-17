---
name: sheet-first-non-repeating-in-stream
title: 'First Non-Repeating Character in a Stream'
tags: [dsa-sheet, stack-and-queue, queues-and-deques]
difficulty: Intermediate
theory: candidates-in-a-stream
---

## Statement

Characters arrive one at a time. After **each** character, write down the **first character that has appeared only once so far**, or `#` if there is none. Return the string of those answers (one per arriving character).

For `"aabc"` the answers are `a`, `#`, `b`, `b`, so the result is `"a#bb"`.

### Examples

**Example 1**

Input:

```python
first_non_repeating_stream('aabc')
```

Output:

```text
'a#bb'
```

**Example 2**

Input:

```python
first_non_repeating_stream('zz')
```

Output:

```text
'z#'
```

### Constraints

- `0 <= len(s) <= 200000`
- `s` contains lower-case letters.

## Explanation

`queue` holds characters seen exactly once so far, plus some that have just been repeated; those are removed lazily from the front before answering.

### Complexity

- Time: O(n). Each character enters and leaves the queue at most once.
- Space: O(k). The counts and the queue hold at most one entry per distinct character, `k` of them.
