---
name: sheet-partition-array
title: 'Partition Around the Last Value'
tags: [dsa-sheet, sorting, divide-and-conquer]
difficulty: Intermediate
---

## Statement

**Partitioning** is the heart of quicksort: pick a _pivot_ value and rearrange the list so that everything smaller or equal comes before it and everything bigger comes after it.

Use this exact method (Lomuto's scheme), with the last value as the pivot:

```python
pivot = a[-1]
i = -1
for j in range(len(a) - 1):
    if a[j] <= pivot:
        i += 1
        a[i], a[j] = a[j], a[i]
a[i + 1], a[-1] = a[-1], a[i + 1]
```

Return `[a, i + 1]`: the rearranged list and the final position of the pivot. Do not change `nums`. The result depends on the exact steps above, so follow them exactly.

### Examples

**Example 1**

Input:

```python
partition_array([3, 7, 1, 5])
```

Output:

```text
[[3, 1, 5, 7], 2]
```

**Explanation:** The pivot is 5. Values 3 and 1 are less than or equal to 5, so they move to the front. The value 7 is greater than 5 and stays near the end, placing the pivot at index 2.

`3` and `1` are `<= 5`, `7` is not. The pivot goes after them.

**Example 2**

Input:

```python
partition_array([4])
```

Output:

```text
[[4], 0]
```

**Explanation:** The input contains a single element 4, which acts as the pivot. It remains in its only position at index 0 without any swaps.

A single value is already in place at index 0.

### Constraints

- `1 <= len(nums) <= 3 * 10**5`
- `-10**9 <= nums[i] <= 10**9`

## Theory

After partitioning, the pivot is in its **final sorted position**: everything before it is `<=` it, everything after is `>` it, and neither side is sorted yet. Quicksort then partitions the left part and the right part the same way. On average this splits the list in about half each time: `O(n log n)`.

Lomuto's scheme keeps a boundary `i`: positions `0..i` hold values `<=` the pivot. Scanning with `j`, every small value is swapped to just past the boundary. It is simple and needs `O(1)` extra memory, but it does more swaps than Hoare's original scheme and it handles many equal values poorly.

Choosing the last value as the pivot is risky: on an already sorted list every partition is lopsided and quicksort degrades to `O(n²)`. Real implementations choose the pivot at random or take a median of a few values.

## Explanation

Copy the list, then run the loop exactly as given. `i + 1` is where the pivot belongs after the final swap, and it is the second item to return.

The final swap `a[i + 1], a[-1] = a[-1], a[i + 1]` also works when `i + 1` is already the last index (it swaps the pivot with itself).

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                     | Variables                      |
| ----------------------------------- | ------------------------------ |
| `a = list(nums)`                    | `a = [3, 7, 1, 5]`             |
| `pivot = a[-1]`                     | `pivot = 5`                    |
| `for j in range(len(a) - 1):`       | `i = -1, j = 0`                |
| `i += 1`                            | `i = 0`                        |
| `for j in range(len(a) - 1):`       | `j = 2`                        |
| `i += 1`                            | `i = 1`                        |
| `a[i + 1], a[-1] = a[-1], a[i + 1]` | `a = [3, 1, 5, 7]`             |
| `return`                            | `returned = [[3, 1, 5, 7], 2]` |

### Complexity

- Time: O(n) where n is the length of nums.
- Extra space: O(n) where n is the length of nums.
- The brute force takes O(n) where n is the length of nums.
