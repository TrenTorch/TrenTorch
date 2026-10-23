---
name: sheet-maximum-xor-with-queries
title: 'Maximum XOR With Each Query'
tags: [dsa-sheet, tries, trie-applications]
difficulty: Advanced
---

## Statement

For each `x` in `queries`, return the **maximum of `x ^ n`** over all numbers `n` in `nums` (`^` is xor). `nums` is not empty.

For `nums = [0, 1, 2, 3, 4]` and `queries = [3, 5]` the answer is `[7, 7]`.

The starter code tries every number for every query. It is correct but too slow for many numbers and queries.

### Examples

**Example 1**

Input:

```python
max_xor_queries([0, 1, 2, 3, 4], [3, 5])
```

Output:

```text
[7, 7]
```

**Example 2**

Input:

```python
max_xor_queries([7], [7, 0])
```

Output:

```text
[0, 7]
```

### Constraints

- `1 <= len(nums) <= 15000`
- `0 <= len(queries) <= 15000`
- `0 <= nums[i], x < 2**30`

## Theory

A **trie** (prefix tree) stores a set of words letter by letter: every node is one letter, a word is a path from the root, and words that share a prefix share the start of their path. Each node has up to 26 children (a dictionary `letter -> node` in Python) and a flag that says "a word ends here". Inserting or searching a word of length `L` takes `O(L)` no matter how many words are stored, and a trie answers **prefix** questions ("does any word start with `ab`?") that a plain set of words cannot answer quickly. A node can be a small dictionary: `node = {}`; mark the end of a word with a special key such as `"$"`.

A trie also works on **binary numbers**: each number is a path of 30 bits from the most significant bit to the least. To maximise `x ^ n`, you want the high bits of the xor to be 1, so at each bit pick the child that is the **opposite** of the bit of `x` if it exists (that bit of the xor is 1), otherwise the same bit.

Insert all numbers (30 steps each) and answer each query by one walk of 30 steps: `O((n + q) × 30)`, instead of `O(n × q)`.

## Explanation

`want = 1 - bit` is the opposite bit. If that child exists, the xor gets a 1 at this position.
