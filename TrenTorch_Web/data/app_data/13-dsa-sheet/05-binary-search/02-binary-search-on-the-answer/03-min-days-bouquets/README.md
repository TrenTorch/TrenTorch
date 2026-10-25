---
name: sheet-min-days-bouquets
title: 'Days to Make Bouquets'
tags: [dsa-sheet, binary-search, binary-search-on-the-answer]
difficulty: Intermediate
---

## Statement

`bloom[i]` is the day on which flower `i` blooms. A bouquet uses `k` **neighbouring** flowers (positions next to each other) that have all bloomed, and each flower can be used in only one bouquet. Return the **earliest day** by which you can make `m` bouquets, or `-1` if it is impossible.

### Examples

**Example 1**

Input:

```python
min_days_bouquets([1, 10, 3, 10, 2], 3, 1)
```

Output:

```text
3
```

**Explanation:** With k=1 each bloomed flower forms a bouquet; by day 3 three flowers have bloomed (days 1,2,3) giving three bouquets.

On day 3 flowers 0, 2 and 4 have bloomed: 3 bouquets of 1.

**Example 2**

Input:

```python
min_days_bouquets([7, 7, 7, 7, 12, 7, 7], 2, 3)
```

Output:

```text
12
```

**Explanation:** Need two bouquets of three adjacent bloomed flowers; until day 12 the flower at position 4 is not bloomed, breaking adjacency, so only one bouquet forms; on day 12 all bloom allowing two bouquets.

On day 12 everything has bloomed: `[7,7,7]` and `[7,7,7]` around the `12`.

### Constraints

- `1 <= len(bloom) <= 2 * 10**4`
- `1 <= bloom[i] <= 10**9`
- `1 <= m, k <= 2 * 10**4`
- Trying every day one by one is too slow for the large tests.

## Theory

Again **binary search on the answer**: the answer is a day, and once enough bouquets are possible on day `d`, they are possible on every later day (flowers do not un-bloom). So "possible by day `d`" goes `False ... False True ... True`.

Impossible is easy to spot first: you need `m * k` flowers, so if `m * k > len(bloom)` return `-1`.

To check a day `d`, sweep the flowers once, counting the current run of bloomed neighbours: a flower with `bloom[i] <= d` extends the run; when the run reaches `k`, count a bouquet and start a new run; an unbloomed flower resets the run. The day range is `min(bloom)` to `max(bloom)`. `O(n log M)`.

## Explanation

If `m * k` is more than the number of flowers, return `-1`. Otherwise search days between the earliest and latest bloom. `possible(day)` counts bouquets in one pass using the run length. A day that works keeps the lower half, a day that does not moves `lo` up.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                   | Variables                                                                 |
| --------------------------------- | ------------------------------------------------------------------------- |
| `def possible(day):`              | `possible = <function min_days_bouquets.<locals>.possible at 0x000001...` |
| `lo, hi = min(bloom), max(bloom)` | `lo = 1, hi = 10`                                                         |
| `mid = (lo + hi) // 2`            | `mid = 5`                                                                 |
| `hi = mid`                        | `hi = 5`                                                                  |
| `hi = mid`                        | `hi = 3, mid = 3`                                                         |
| `mid = (lo + hi) // 2`            | `mid = 2`                                                                 |
| `lo = mid + 1`                    | `lo = 3`                                                                  |
| `return`                          | `returned = 3`                                                            |

### Complexity

- Time: O(n log D) where n is bloom length, D is max-min bloom day.
- Extra space: O(1) constant extra space.
- The brute force takes O(n^2) where n is bloom length.
