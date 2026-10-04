---
name: dsa-linked-list-sum
title: 'Add Two Numbers (Linked List)'
tags: [dsa]
difficulty: Intermediate
---

## Statement

Add two numbers represented as reversed linked lists. 342 + 465 = 807 is represented as 2→4→3 + 5→6→4 = 7→0→8 (reversed). Implement addition digit-by-digit with carry.

## Theory

### Linked lists for number representation

Storing numbers in reverse (least significant digit first) simplifies addition: traverse both lists once, adding corresponding digits.

`
342 → 2→4→3

- 465 → 5→6→4
  = 807 → 7→0→8
  `

### Algorithm

1. Initialize carry = 0
2. Traverse both lists simultaneously
3. Sum digit1 + digit2 + carry; create new node for (sum % 10), update carry = sum / 10
4. Handle remaining digits if one list is longer
5. Handle final carry if it exists

Time O(max(len(l1), len(l2))), space O(same).

### Why this matters

- Linked lists don't require preallocated size
- Simpler than array-based addition
- Traversal order matches digit order
- Educational: understand carry propagation and node creation

### Reverse vs non-reverse

With numbers in normal order (least significant digit last), addition requires reversing or traversing backward.

## Explanation

The solution creates a dummy node, iterates through both lists adding digits with carry, creates new nodes for results, and returns dummy.next.
