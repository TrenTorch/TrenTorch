---
name: sheet-stock-span
title: 'Stock Span'
tags: [dsa-sheet, stack-and-queue, monotonic-stack]
difficulty: Intermediate
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

## Theory

A **stack** is last in, first out: you only add (`push`) and remove (`pop`) at the top. In Python a list does this with `append()` and `pop()`, both `O(1)`.

The span of day `i` reaches back to the nearest earlier day with a **strictly higher** price (the "previous greater element"). Everything between them is at most `prices[i]`. So `span = i - previous_greater_index` (use `-1` if there is none).

Find it with a monotonic stack of indices: pop all indices whose price is `<=` the current price (they cannot block later days either, since the current day is at least as high and later), then the top, if any, is the previous greater. Push the current index. `O(n)`.

## Explanation

The stack keeps indices with strictly decreasing prices. After popping the smaller or equal ones, the top is the nearest higher price on the left.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                 | Variables                                                 |
| ----------------------------------------------- | --------------------------------------------------------- |
| `out = []`                                      | `out = []`                                                |
| `stack.append(i)`                               | `out = [1], stack = [0], i = 0, p = 100`                  |
| `for i, p in enumerate(prices):`                | `out = [1, 1], stack = [0, 1], i = 2, p = 60`             |
| `stack.pop()`                                   | `out = [1, 1, 1], i = 3, p = 70`                          |
| `out.append(i - stack[-1] if stack else i + 1)` | `out = [1, 1, 1, 2, 1], stack = [0, 1, 3], i = 4, p = 60` |
| `stack.pop()`                                   | `stack = [0, 1], i = 5, p = 75`                           |
| `stack.pop()`                                   | `out = [1, 1, 1, 2, 1, 4], i = 6, p = 85`                 |
| `return`                                        | `returned = [1, 1, 1, 2, 1, 4, 6]`                        |

### Complexity

- Time: O(n) time where n is number of prices.
- Extra space: O(n) extra space where n is number of prices.
- The brute force takes O(n^2) time where n is number of prices.
