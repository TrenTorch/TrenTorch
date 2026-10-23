---
name: sheet-search-suggestions-system
title: 'Search Suggestions'
tags: [dsa-sheet, tries, trie-basics]
difficulty: Intermediate
---

## Statement

A user types `search_word` one letter at a time. After **each** letter, suggest **up to three** products that start with what has been typed so far, in **dictionary order**. Return the list of suggestion lists (one per letter). Repeated product names are kept.

For `products = ["mobile", "mouse", "moneypot", "monitor", "mousepad"]` and `search_word = "mouse"` the answer is `[["mobile", "moneypot", "monitor"], ["mobile", "moneypot", "monitor"], ["mouse", "mousepad"], ["mouse", "mousepad"], ["mouse", "mousepad"]]`.

The starter code scans and sorts all products after every letter. It is correct but too slow for many products.

### Examples

**Example 1**

Input:

```python
suggested_products(['mobile', 'mouse', 'moneypot', 'monitor', 'mousepad'], 'mouse')
```

Output:

```text
[['mobile', 'moneypot', 'monitor'], ['mobile', 'moneypot', 'monitor'], ['mouse', 'mousepad'], ['mouse', 'mousepad'], ['mouse', 'mousepad']]
```

**Example 2**

Input:

```python
suggested_products(['havana'], 'tatiana')
```

Output:

```text
[[], [], [], [], [], [], []]
```

### Constraints

- `0 <= len(products) <= 100000`
- `0 <= len(search_word) <= 20`
- Lower-case letters, 1 to 20 long.

## Theory

A **trie** (prefix tree) stores a set of words letter by letter: every node is one letter, a word is a path from the root, and words that share a prefix share the start of their path. Each node has up to 26 children (a dictionary `letter -> node` in Python) and a flag that says "a word ends here". Inserting or searching a word of length `L` takes `O(L)` no matter how many words are stored, and a trie answers **prefix** questions ("does any word start with `ab`?") that a plain set of words cannot answer quickly. A node can be a small dictionary: `node = {}`; mark the end of a word with a special key such as `"$"`.

Sort the products once. All products with a given prefix then form **one contiguous block** of the sorted list. After each new letter the block can only shrink: find its start with a **binary search** (`bisect_left` of the prefix), and the suggestions are the next up to three items as long as they start with the prefix.

This is `O(n log n)` for the sort plus `O(len(word) × log n)` for the searches. A trie that stores the three smallest words at each node works too, but the sorted-list view is shorter.

## Explanation

`bisect_left(products, prefix)` is the first product that could start with `prefix`. Slicing three items and filtering by prefix gives the suggestions.
