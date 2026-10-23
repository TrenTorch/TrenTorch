---
name: sheet-word-break
title: 'Word Break'
tags: [dsa-sheet, dynamic-programming, sequences-and-counting]
difficulty: Intermediate
---

## Statement

Return `True` if the string `s` can be **split into a sequence of words from `words`** (words may be reused any number of times).

For `s = "leetcode"` and `words = ["leet", "code"]` the answer is `True`; for `s = "catsandog"` and `words = ["cats", "dog", "sand", "and", "cat"]` it is `False`.

The starter code tries every split without remembering failures. It is correct but too slow on strings that cannot be split.

### Examples

**Example 1**

Input:

```python
word_break('leetcode', ['leet', 'code'])
```

Output:

```text
True
```

**Example 2**

Input:

```python
word_break('catsandog', ['cats', 'dog', 'sand', 'and', 'cat'])
```

Output:

```text
False
```

### Constraints

- `0 <= len(s) <= 20000`
- `0 <= len(words) <= 1000`
- `1 <= len(word) <= 20`, lower-case letters.

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

**State:** `can(i)`, whether the first `i` characters can be split. **Transition:** `can(i)` is true if some `j < i` has `can(j)` true **and** `s[j:i]` is a word. **Base case:** `can(0) = True`. **Answer:** `can(len(s))`.

A set makes the word lookup `O(1)` (the substring itself costs `O(length)`). Since words are at most `maxlen` long, only the last `maxlen` positions `j` need to be tried: `O(n × maxlen)`.

The recursion without a cache fails on strings like `"aaaa...b"` with words `["a", "aa", ...]`: it explores an exponential number of ways to split the `a`s before discovering that the `b` cannot be matched.

## Explanation

`can[i]` is filled left to right. The inner loop stops after `maxlen` characters because no word is longer.
