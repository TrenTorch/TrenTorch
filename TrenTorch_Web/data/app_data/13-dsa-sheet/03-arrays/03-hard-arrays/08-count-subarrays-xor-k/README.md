---
name: sheet-count-subarrays-xor-k
title: 'Subarrays With XOR K'
tags: [dsa-sheet, arrays, hard-arrays]
difficulty: Advanced
---

## Statement

The **XOR** of a run is all its values combined with the `^` operator. Return how many contiguous runs of `nums` have an XOR equal to `k`.

The starter code tries every start and end. It is correct but too slow. Make it fast.

### Examples

**Example 1**

Input:

```python
count_subarrays_xor_k([4, 2, 2, 6, 4], 6)
```

Output:

```text
4
```

**Explanation:** Cumulative XOR tracking with a hashmap counts subarrays where prefix XOR XOR k has been seen before, yielding exactly four matches for this input.

The runs are `[4, 2]`, `[4, 2, 2, 6]`, `[2, 2, 6]` and `[6]`.

**Example 2**

Input:

```python
count_subarrays_xor_k([5, 6, 7, 8, 9], 5)
```

Output:

```text
2
```

**Explanation:** Cumulative XOR tracking with a hashmap counts subarrays where prefix XOR XOR k has been seen before, yielding exactly two matches for this input.

The runs are `[5]` and `[5, 6, 7, 8, 9]`.

### Constraints

- `0 <= len(nums) <= 2 * 10**5`
- `0 <= nums[i] <= 10**9`
- `0 <= k <= 2**30`

## Theory

The counting-subarrays trick works for any operation that can be **undone**. For sums the undo is subtraction; for XOR it is XOR itself, because `x ^ x = 0`.

Let `prefix[i]` be the XOR of the first `i` values. The XOR of the run from `a` up to `b` is `prefix[a] ^ prefix[b]` (the shared front part cancels). It equals `k` exactly when `prefix[a] = prefix[b] ^ k`.

So keep a dictionary counting each prefix XOR seen so far, start it with `{0: 1}`, and for each new prefix add `seen[prefix ^ k]` to the answer before recording the prefix. `O(n)`.

## Explanation

`prefix` is the XOR of everything read so far. Runs ending here that XOR to `k` are those starting after an earlier prefix equal to `prefix ^ k`, and `seen` counts them. The lookup comes before recording the current prefix, as with sums.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                          | Variables                                                |
| ---------------------------------------- | -------------------------------------------------------- |
| `seen = {0: 1}`                          | `seen = {0: 1}`                                          |
| `prefix ^= x`                            | `prefix = 4, count = 0, x = 4`                           |
| `for x in nums:`                         | `seen = {0: 1, 4: 1}, x = 2`                             |
| `seen[prefix] = seen.get(prefix, 0) + 1` | `seen = {0: 1, 4: 1, 6: 1}, prefix = 6, count = 1`       |
| `for x in nums:`                         | `seen = {0: 1, 4: 2, 6: 1}, prefix = 4, x = 6`           |
| `seen[prefix] = seen.get(prefix, 0) + 1` | `seen = {0: 1, 4: 2, 6: 1, 2: 1}, prefix = 2, count = 3` |
| `prefix ^= x`                            | `prefix = 6, x = 4`                                      |
| `return`                                 | `returned = 4`                                           |

### Complexity

- Time: O(n) where n is length of nums.
- Extra space: O(n) where n is nums length for seen map.
- The brute force takes O(n^2) where n is nums length.
