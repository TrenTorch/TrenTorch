---
name: sheet-rearrange-by-sign
title: 'Rearrange by Sign'
tags: [dsa-sheet, arrays, array-patterns]
difficulty: Intermediate
---

## Statement

Rearrange `nums` so that **non-negative** values (`>= 0`) and **negative** values (`< 0`) alternate, starting with a non-negative one. Inside each group keep the original order. If one group runs out first, put the rest of the other group at the end, in order.

Return a new list.

### Examples

**Example 1**

Input:

```python
rearrange_by_sign([3, 1, -2, -5, 2, -4])
```

Output:

```text
[3, -2, 1, -5, 2, -4]
```

Non-negative: 3, 1, 2. Negative: -2, -5, -4. Interleaved: 3, -2, 1, -5, 2, -4.

**Example 2**

Input:

```python
rearrange_by_sign([1, 2, 3, -1])
```

Output:

```text
[1, -1, 2, 3]
```

After `1, -1` the negatives run out, so `2, 3` follow.

### Constraints

- `0 <= len(nums) <= 3 * 10**5`
- `-10**9 <= nums[i] <= 10**9`

## Theory

Splitting into two lists with a comprehension each keeps the order inside each group. Then you **interleave** them: take one from each in turn.

The interleave is a two-pointer idea with one pointer per list. In Python `itertools.zip_longest` does it, or an index loop that appends `pos[i]` and `neg[i]` when they exist. The leftover of the longer list is added automatically because the loop runs for the longer length.

The in-place version of this problem is much harder, because you must preserve order while moving values; the output-list version is the one to know first.

## Explanation

`pos` and `neg` hold the two groups in order. The loop runs for `max(len(pos), len(neg))` steps and appends `pos[i]` then `neg[i]` when they exist, so the alternation starts with a non-negative value and the longer group's tail follows.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                            | Variables                          |
| ------------------------------------------ | ---------------------------------- |
| `pos = [x for x in nums if x >= 0]`        | `pos = [3, 1, 2]`                  |
| `out = []`                                 | `neg = [-2, -5, -4], out = []`     |
| `for i in range(max(len(pos), len(neg))):` | `i = 0`                            |
| `out.append(neg[i])`                       | `out = [3, -2]`                    |
| `out.append(pos[i])`                       | `out = [3, -2, 1], i = 1`          |
| `for i in range(max(len(pos), len(neg))):` | `out = [3, -2, 1, -5], i = 2`      |
| `out.append(pos[i])`                       | `out = [3, -2, 1, -5, 2]`          |
| `return`                                   | `returned = [3, -2, 1, -5, 2, -4]` |

### Complexity

- Time: O(n) where n is length of nums.
- Extra space: O(n) where n is length of nums.
- The brute force takes O(n) where n is length of nums.
