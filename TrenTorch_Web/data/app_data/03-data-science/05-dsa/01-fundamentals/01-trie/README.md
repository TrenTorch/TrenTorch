---
name: dsa-trie
title: 'Implement a Trie (Prefix Tree)'
tags: [dsa]
difficulty: Intermediate
---

## Statement

Build a data structure for fast word lookups and autocomplete. A Trie stores words as nested nodes, where each path from root to a node represents a prefix. Implement insert(word), search(word), and startsWith(prefix) in O(m) time, where m is word length.

## Theory

### Tries enable prefix-based operations

A Trie (prefix tree) is a tree where each node represents a character. Words are stored as paths from root to leaf.

`Example: Insert 'cat', 'car', 'card'
    root
     |
     c
     |
     a
    / \
   t   r
      /
     d`

### Operations

- Insert: traverse/create nodes for each character, mark end-of-word
- Search: traverse path; if all characters exist and node is marked, word exists
- StartsWith: traverse path; if all characters exist, prefix exists

Both are O(m) where m is the word length.

### Why Tries matter

- Autocomplete: prefix matching in O(m)
- Spell-checkers: word existence in O(m)
- IP routing: efficient longest-prefix matching
- Better than HashSet for prefix queries

### Space-time trade-off

Tries use more space (one node per character) but enable prefix operations HashSets can't.

## Explanation

The solution implements a TrieNode class where each node has a map of children and an is_end_of_word flag. Insert, search, and startsWith traverse the tree character-by-character.
