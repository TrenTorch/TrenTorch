---
name: sheet-reveal-cards-in-increasing-order
title: 'Reveal Cards in Increasing Order'
tags: [dsa-sheet, stack-and-queue, queues-and-deques]
difficulty: Advanced
theory: simulating-a-deck-of-cards
---

## Statement

You have a deck of cards with different numbers. You may order the deck any way you like, then repeat these steps until all cards are revealed: **take the top card, reveal it and remove it; then, if cards remain, move the next top card to the bottom of the deck**.

Return the order of the deck (top first) for which the revealed cards come out in **increasing order**.

For `[17, 13, 11, 2, 3, 5, 7]` the answer is `[2, 13, 3, 11, 5, 17, 7]`.

### Examples

**Example 1**

Input:

```python
reveal_cards([17, 13, 11, 2, 3, 5, 7])
```

Output:

```text
[2, 13, 3, 11, 5, 17, 7]
```

**Example 2**

Input:

```python
reveal_cards([1, 1000])
```

Output:

```text
[1, 1000]
```

### Constraints

- `0 <= len(deck) <= 100000`
- All values are different, `1 <= deck[i] <= 10**9`.

## Explanation

The simulation uses indices of the result list. `popleft` reveals a card; `append(popleft())` moves the next card to the bottom.

### Complexity

- Time: O(n log n). Sorting dominates; the queue simulation is O(n).
- Space: O(n). The queue of positions and the result.
