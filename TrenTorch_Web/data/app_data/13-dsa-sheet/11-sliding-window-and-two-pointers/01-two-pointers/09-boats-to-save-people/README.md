---
name: sheet-boats-to-save-people
title: 'Boats to Save People'
tags: [dsa-sheet, two-pointers, two-pointers]
difficulty: Intermediate
---

## Statement

`people[i]` is the weight of person `i`. Each boat carries **at most two people** and a total weight of at most `limit`. Every person weighs at most `limit`. Return the **fewest boats** needed to carry everyone.

For `people = [3, 2, 2, 1]` and `limit = 3` the answer is `3` (`[1, 2]`, `[2]`, `[3]`).

### Examples

**Example 1**

Input:

```python
boats_needed([3, 2, 2, 1], 3)
```

Output:

```text
3
```

**Example 2**

Input:

```python
boats_needed([3, 5, 3, 4], 5)
```

Output:

```text
4
```

### Constraints

- `0 <= len(people) <= 200000`
- `1 <= people[i] <= limit <= 30000`

## Theory

**Two pointers** means keeping two positions in the data (often one at each end, or one behind the other) and moving them according to a rule, so that each position moves at most `n` times in total. That turns a double loop (`O(n²)`) into a single pass (`O(n)`).

Sort the weights. Look at the **heaviest** person: the best partner for them is the **lightest** one, because the lightest person is the one most likely to fit. If heaviest + lightest fits in a boat, they go together; if not, no one else fits with the heaviest either (everyone else is heavier than the lightest), so the heaviest goes alone.

Use two pointers at the ends: every step uses one boat, always takes the heaviest, and takes the lightest too when it fits. This is a **greedy** choice backed by the sorted order. `O(n log n)` for the sort, `O(n)` for the pass.

## Explanation

`heavy` always boards. `light` boards with them only if the sum fits; otherwise the heavy person leaves alone and `light` waits for the next, lighter, heavy person.
