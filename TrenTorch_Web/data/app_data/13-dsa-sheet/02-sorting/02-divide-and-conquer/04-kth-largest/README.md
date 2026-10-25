---
name: sheet-kth-largest
title: 'Kth Largest Value'
tags: [dsa-sheet, sorting, divide-and-conquer]
difficulty: Intermediate
---

## Statement

Return the `k`-th largest value in `nums`, where `k = 1` is the largest. Equal values count separately: in `[5, 5, 3]` the 2nd largest is `5` and the 3rd largest is `3`.

Sorting the whole list works, but you only need one value. See if you can do it faster.

### Examples

**Example 1**

Input:

```python
kth_largest([3, 2, 1, 5, 6, 4], 2)
```

Output:

```text
5
```

**Explanation:** Sorting the list in descending order places 6 first, 5 second, 4 third, 3 fourth, 2 fifth, and 1 sixth. Since k is 2, the output is 5.

Sorted from largest: 6, 5, 4, 3, 2, 1. The 2nd is 5.

**Example 2**

Input:

```python
kth_largest([5, 5, 3], 3)
```

Output:

```text
3
```

**Explanation:** The list contains 5, 5, and 3 in descending order. The third largest value is 3.

Sorted from largest: 5, 5, 3. The 3rd is 3.

### Constraints

- `1 <= k <= len(nums) <= 2 * 10**5`
- `-10**9 <= nums[i] <= 10**9`

## Theory

Sorting finds the `k`-th largest in `O(n log n)`, but it puts _every_ value in order when you want just one. **Quickselect** borrows quicksort's partition step and recurses into only the side that holds the answer, so on average it does `n + n/2 + n/4 + ... = O(n)` work.

Pick a pivot and split the values into smaller, equal and bigger. If `k` falls in the bigger group, continue there. If it falls in the equal group, the pivot is the answer. Otherwise continue in the smaller group with `k` reduced by the sizes you skipped. Splitting into three groups (not two) keeps lists with many equal values fast.

The worst case is `O(n²)` if the pivots are always bad, so real code picks them at random or uses the median-of-medians method. A heap of size `k` (`heapq.nlargest`) is another good choice, at `O(n log k)`.

## Explanation

Convert to an ascending index: the `k`-th largest is at index `len - k` in sorted order. Pick the middle value as pivot and split into `less`, `equal` count, and `greater`. If the target index is inside `less`, loop on `less`. If it is inside the equal block, return the pivot. Otherwise subtract the sizes of `less` and the equal block from the target and loop on `greater`.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                      | Variables                |
| ------------------------------------ | ------------------------ |
| `a = list(nums)`                     | `a = [3, 2, 1, 5, 6, 4]` |
| `target = len(a) - k`                | `target = 4`             |
| `pivot = a[len(a) // 2]`             | `pivot = 5`              |
| `less = [x for x in a if x < pivot]` | `less = [3, 2, 1, 4]`    |
| `equal = a.count(pivot)`             | `equal = 1`              |
| `return`                             | `returned = 5`           |

### Complexity

- Time: O(n) average where n is the number of elements in nums.
- Extra space: O(n) where n is the number of elements in nums.
- The brute force takes O(n log n) where n is the number of elements in nums.
