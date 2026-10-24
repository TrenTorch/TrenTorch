---
name: sheet-longest-unique-substring
title: 'Longest Substring Without Repeats'
tags: [dsa-sheet, basics, make-it-fast]
difficulty: Intermediate
---

## Statement

Given a string `s`, return the length of the longest substring (a run of consecutive characters) in which all characters are different.

The starter code restarts from every position and grows until it hits a repeat. Make it fast.

### Examples

**Example 1**

Input:

```python
longest_unique_substring('abcabcbb')
```

Output:

```text
3
```

The longest is `abc`.

**Example 2**

Input:

```python
longest_unique_substring('bbbbb')
```

Output:

```text
1
```

The longest is `b`.

**Example 3**

Input:

```python
longest_unique_substring('pwwkew')
```

Output:

```text
3
```

The longest is `wke`.

### Constraints

- `0 <= len(s) <= 2 * 10**5`
- `s` can contain any characters.

## Theory

Restarting from every position repeats a lot of work. If you are scanning `abcdeb` and meet the second `b`, you do not need to go back to `b` and start over: the run can simply continue from just after the first `b`.

That is a **sliding window**: keep a window `[start, i]` with no repeats and move its left edge only forward. Store the last position of each character in a dictionary. When the current character was last seen inside the window, jump `start` to one past that position. Every character is visited once, so the time is `O(n)`.

## Explanation

`last[ch]` is the last index where `ch` appeared. If `last[ch] >= start`, then `ch` is already in the current window, so move `start` to `last[ch] + 1`. Then record `last[ch] = i` and update the best length `i - start + 1`.

The check `last[ch] >= start` matters: a character seen long ago, before the window began, must not move `start` backwards.
