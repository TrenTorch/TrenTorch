---
name: sheet-bubble-sort-passes
title: 'How Many Bubble Sort Passes?'
tags: [dsa-sheet, sorting, sorting-by-hand]
difficulty: Beginner
theory: how-many-passes
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

## Explanation

In each pass, an element that has a bigger value somewhere before it moves exactly one place to the left. So the number of passes that make a swap is the largest "how many bigger values are before me" over all elements, and the final pass without swaps adds one.

A Fenwick tree over the ranks of the values counts "bigger values before me" in `O(log n)` per element. Simulating the passes one by one also works at this size, in `O(n^2)`.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                              | Variables                                                                |
| ------------------------------------------------------------ | ------------------------------------------------------------------------ |
| `rank = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}` | `rank = {1: 1, 2: 2, 3: 3}`                                              |
| `for seen, x in enumerate(nums):`                            | `size = 3, tree = [0, 0, 0, 0], most_bigger_before = 0, seen = 0, x = 3` |
| `i -= i & -i`                                                | `i = 0, not_bigger = 0`                                                  |
| `for seen, x in enumerate(nums):`                            | `tree = [0, 0, 0, 1], seen = 1, x = 2, i = 4`                            |
| `i = rank[x]`                                                | `most_bigger_before = 1, i = 2`                                          |
| `i = rank[x]`                                                | `tree = [0, 0, 1, 1], seen = 2, x = 1, i = 1`                            |
| `tree[i] += 1`                                               | `tree = [0, 1, 1, 1], most_bigger_before = 2`                            |
| `return`                                                     | `returned = 3`                                                           |

### Complexity

- Time: O(n log n). Each element moves left by exactly one place per pass, so the number of passes is `1 +` the largest count of bigger values to the left of any element; a Fenwick tree counts those in `log n` per element.
- Space: O(n). The Fenwick tree and the rank table.
