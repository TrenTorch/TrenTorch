---
name: sheet-first-non-repeating-in-stream
title: 'First Non-Repeating Character in a Stream'
tags: [dsa-sheet, stack-and-queue, queues-and-deques]
difficulty: Intermediate
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

## Theory

A **queue** keeps things in arrival order, and we need the oldest candidate. Keep a count of each character and a queue of characters in the order they first arrived. When a character arrives, count it and add it to the queue if it is new. Then look at the **front** of the queue: while the front has a count above 1 it can never be the answer again, so **remove it** from the front. The front that remains (if any) is the answer.

Each character enters the queue once and leaves it once, so the whole thing is `O(n)`. Do not search the queue: removing from the front as needed is enough.

## Explanation

`queue` holds characters seen exactly once so far, plus some that have just been repeated; those are removed lazily from the front before answering.
