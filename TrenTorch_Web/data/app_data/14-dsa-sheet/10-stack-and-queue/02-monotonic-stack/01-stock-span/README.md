---
name: sheet-stock-span
title: 'Stock Span'
tags: [dsa-sheet, stack-and-queue, monotonic-stack]
difficulty: Intermediate
theory: looking-to-the-left
---

## Statement

For each day `i`, the **span** is the number of consecutive days ending at day `i` (including day `i`) whose price was **less than or equal to** `prices[i]`.

For `[100, 80, 60, 70, 60, 75, 85]` the spans are `[1, 1, 1, 2, 1, 4, 6]`.

The starter code walks back from every day. It is correct but too slow for long lists.

### Examples

**Example 1**

Input:

```python
stock_span([100, 80, 60, 70, 60, 75, 85])
```

Output:

```text
[1, 1, 1, 2, 1, 4, 6]
```

**Example 2**

Input:

```python
stock_span([1, 2, 3])
```

Output:

```text
[1, 2, 3]
```

### Constraints

- `0 <= len(prices) <= 200000`
- `1 <= prices[i] <= 10**9`

## Explanation

The stack keeps indices with strictly decreasing prices. After popping the smaller or equal ones, the top is the nearest higher price on the left.

### Complexity

- Time: O(n). Each index is pushed once and popped at most once.
- Space: O(n). The stack and the result.
