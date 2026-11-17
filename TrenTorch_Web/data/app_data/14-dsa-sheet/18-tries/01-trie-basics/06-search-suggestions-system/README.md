---
name: sheet-search-suggestions-system
title: 'Search Suggestions'
tags: [dsa-sheet, tries, trie-basics]
difficulty: Intermediate
theory: suggestions-after-every-typed-letter
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

## Explanation

`bisect_left(products, prefix)` is the first product that could start with `prefix`. Slicing three items and filtering by prefix gives the suggestions.

### Complexity

- Time: O(P log P + k * L * log P). `P` = number of products, sorted once; after each typed letter one binary search finds the first match (`L` = length of the search word).
- Space: O(P). The sorted list (the answer is output).
