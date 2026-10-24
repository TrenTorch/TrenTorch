---
name: sheet-bubble-sort-passes
title: 'How Many Bubble Sort Passes?'
tags: [dsa-sheet, sorting, sorting-by-hand]
difficulty: Beginner
---

## Statement

**Bubble sort** walks along the list comparing neighbours. Whenever the left one is bigger than the right one it swaps them. One walk from start to end is a **pass**. It stops after the first pass in which nothing was swapped.

```python
passes = 0
while True:
    passes += 1
    swapped = False
    for i in range(len(a) - 1):
        if a[i] > a[i + 1]:
            a[i], a[i + 1] = a[i + 1], a[i]
            swapped = True
    if not swapped:
        break
```

Return the final value of `passes`, counting the last pass that swapped nothing. A list that is already sorted, and a list with fewer than two items, takes `1` pass.

### Examples

**Example 1**

Input:

```python
bubble_sort_passes([3, 2, 1])
```

Output:

```text
3
```

Pass 1 gives `[2, 1, 3]`, pass 2 gives `[1, 2, 3]`, pass 3 swaps nothing: 3 passes.

**Example 2**

Input:

```python
bubble_sort_passes([1, 2, 3])
```

Output:

```text
1
```

No swaps in the first pass, so it stops after 1.

### Constraints

- `0 <= len(nums) <= 1500`
- `-10**9 <= nums[i] <= 10**9`

## Theory

After the first pass the largest value has "bubbled" to the end, after the second pass the second largest is in place, and so on. Each pass fixes at least one more value, so there are at most `n` passes, and each pass costs `n - 1` comparisons: `O(n²)` in the worst case.

The `swapped` flag gives it a fast path. If the input is already sorted, one pass finds nothing to swap and stops in `O(n)`.

A value only moves left by **one place per pass**. So a small value that starts far to the right needs many passes to arrive. The number of passes is decided by the element that has to travel left the farthest, and you can read that distance straight from the input without simulating.

## Explanation

Simulating is fine at this size: copy the list, run the passes exactly as written, and count them.

There is also a shortcut. In each pass, an element that has a bigger value somewhere before it moves exactly one place left. So the number of passes with swaps is the largest "how many bigger values are before me" over all elements, and the final pass without swaps adds one.
