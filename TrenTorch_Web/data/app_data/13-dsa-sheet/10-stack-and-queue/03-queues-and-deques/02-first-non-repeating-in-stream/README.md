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

**Explanation:** For 'aabc', 'a' is unique initially, then 'a' repeats leaving nothing unique, then 'b' becomes the first unique character.

**Example 2**

Input:

```python
first_non_repeating_stream('zz')
```

Output:

```text
'z#'
```

**Explanation:** For 'zz', 'z' is unique at the first step but repeats at the second leaving no unique characters.

### Constraints

- `0 <= len(s) <= 200000`
- `s` contains lower-case letters.

## Theory

A **queue** keeps things in arrival order, and we need the oldest candidate. Keep a count of each character and a queue of characters in the order they first arrived. When a character arrives, count it and add it to the queue if it is new. Then look at the **front** of the queue: while the front has a count above 1 it can never be the answer again, so **remove it** from the front. The front that remains (if any) is the answer.

Each character enters the queue once and leaves it once, so the whole thing is `O(n)`. Do not search the queue: removing from the front as needed is enough.

## Explanation

`queue` holds characters seen exactly once so far, plus some that have just been repeated; those are removed lazily from the front before answering.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                          | Variables                                                                |
| ---------------------------------------- | ------------------------------------------------------------------------ |
| `counts = {}`                            | `counts = {}`                                                            |
| `for ch in s:`                           | `queue = deque([]), out = [], ch = 'a'`                                  |
| `queue.append(ch)`                       | `counts = {'a': 1}, queue = deque(['a'])`                                |
| `queue.popleft()`                        | `counts = {'a': 2}, queue = deque([]), out = ['a']`                      |
| `for ch in s:`                           | `out = ['a', '#'], ch = 'b'`                                             |
| `out.append(queue[0] if queue else "#")` | `counts = {'a': 2, 'b': 1}, queue = deque(['b']), out = ['a', '#', 'b']` |
| `counts[ch] = counts.get(ch, 0) + 1`     | `counts = {'a': 2, 'b': 1, 'c': 1}, ch = 'c'`                            |
| `return`                                 | `returned = 'a#bb'`                                                      |

### Complexity

- Time: O(n), where n is the length of the string.
- Extra space: O(k), where k is the number of unique characters.
- The brute force takes O(n^2), where n is the length of the string.
