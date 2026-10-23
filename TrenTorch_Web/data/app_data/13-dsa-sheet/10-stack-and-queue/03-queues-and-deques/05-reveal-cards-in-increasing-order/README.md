---
name: sheet-reveal-cards-in-increasing-order
title: 'Reveal Cards in Increasing Order'
tags: [dsa-sheet, stack-and-queue, queues-and-deques]
difficulty: Advanced
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

## Theory

Run the process on **positions** instead of on numbers. Simulate it on the list `0, 1, ..., n - 1` with a deque: the position revealed first gets the smallest card, the position revealed second the second smallest, and so on.

So: sort the deck. Put the positions `0..n-1` in a deque. Repeat: take the front position `p` and give it the next smallest card (`result[p] = next card`); then, if the deque is not empty, move its new front to the back. Stop when all positions are used.

The deque makes both "take from the top" and "move to the bottom" `O(1)`, so the whole thing is `O(n log n)` for the sort plus `O(n)`.

## Explanation

The simulation uses indices of the result list. `popleft` reveals a card; `append(popleft())` moves the next card to the bottom.
