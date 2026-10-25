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

**Explanation:** For [17,13,11,2,3,5,7] the algorithm sorts cards and assigns positions via move-to-bottom pattern yielding [2,13,3,11,5,17,7] because smallest card revealed first and pattern orders others

**Example 2**

Input:

```python
reveal_cards([1, 1000])
```

Output:

```text
[1, 1000]
```

**Explanation:** For [1,1000] only two cards exist process reveals top card first moves next to bottom if remaining so initial order [1,1000] directly reveals 1 then 1000 in increasing order

### Constraints

- `0 <= len(deck) <= 100000`
- All values are different, `1 <= deck[i] <= 10**9`.

## Theory

Run the process on **positions** instead of on numbers. Simulate it on the list `0, 1, ..., n - 1` with a deque: the position revealed first gets the smallest card, the position revealed second the second smallest, and so on.

So: sort the deck. Put the positions `0..n-1` in a deque. Repeat: take the front position `p` and give it the next smallest card (`result[p] = next card`); then, if the deque is not empty, move its new front to the back. Stop when all positions are used.

The deque makes both "take from the top" and "move to the bottom" `O(1)`, so the whole thing is `O(n log n)` for the sort plus `O(n)`.

## Explanation

The simulation uses indices of the result list. `popleft` reveals a card; `append(popleft())` moves the next card to the bottom.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                      | Variables                                                                            |
| ------------------------------------ | ------------------------------------------------------------------------------------ |
| `n = len(deck)`                      | `n = 7`                                                                              |
| `for card in sorted(deck):`          | `result = [0, 0, 0, 0, 0, 0, 0], positions = deque([0, 1, 2, 3, 4, 5, 6]), card = 2` |
| `for card in sorted(deck):`          | `result = [2, 0, 0, 0, 0, 0, 0], positions = deque([2, 3, 4, 5, 6, 1]), card = 3`    |
| `for card in sorted(deck):`          | `result = [2, 0, 3, 0, 0, 0, 0], positions = deque([4, 5, 6, 1, 3]), card = 5`       |
| `result[positions.popleft()] = card` | `result = [2, 0, 3, 0, 5, 0, 7], positions = deque([1, 3, 5]), card = 7`             |
| `result[positions.popleft()] = card` | `result = [2, 0, 3, 11, 5, 0, 7], positions = deque([5, 1]), card = 11`              |
| `result[positions.popleft()] = card` | `result = [2, 13, 3, 11, 5, 0, 7], positions = deque([5]), card = 13`                |
| `return`                             | `returned = [2, 13, 3, 11, 5, 17, 7]`                                                |

### Complexity

- Time: O(n log n).
- Extra space: O(n).
- The brute force takes O(n! * n).
