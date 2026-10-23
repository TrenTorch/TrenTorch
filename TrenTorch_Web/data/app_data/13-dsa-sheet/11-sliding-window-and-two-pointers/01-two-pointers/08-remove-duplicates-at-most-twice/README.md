---
name: sheet-remove-duplicates-at-most-twice
title: 'Keep at Most Two of Each Value'
tags: [dsa-sheet, two-pointers, two-pointers]
difficulty: Intermediate
---

## Statement

`nums` is sorted in increasing order. Return the list where each value appears **at most twice** (extra copies removed), keeping the order. For `[1, 1, 1, 2, 2, 3]` the answer is `[1, 1, 2, 2, 3]`.

Try to solve it with one pass and two pointers: a **write** pointer for the answer and a **read** pointer for the input.

### Examples

**Example 1**

Input:

```python
keep_at_most_twice([1, 1, 1, 2, 2, 3])
```

Output:

```text
[1, 1, 2, 2, 3]
```

**Example 2**

Input:

```python
keep_at_most_twice([0, 0, 1, 1, 1, 1, 2, 3, 3])
```

Output:

```text
[0, 0, 1, 1, 2, 3, 3]
```

### Constraints

- `0 <= len(nums) <= 200000`
- `nums` is sorted in increasing order.

## Theory

**Two pointers** means keeping two positions in the data (often one at each end, or one behind the other) and moving them according to a rule, so that each position moves at most `n` times in total. That turns a double loop (`O(n²)`) into a single pass (`O(n)`).

The two pointers here are a **reader** that scans every value and a **writer** that marks where the next kept value goes. A value is kept if fewer than two copies of it are already kept. In a sorted list the earlier kept copies are right behind the writer, so the test is simply: `write < 2 or nums[read] != nums[write - 2]`.

If so, copy it to `nums[write]` and advance the writer. This "read ahead, write behind" pattern edits a list in place in `O(n)`. Changing the "2" to any `k` gives "at most `k` copies".

## Explanation

`a[write - 2]` is the second-to-last kept value. If the new value differs from it, there are fewer than two copies of the new value kept (the list is sorted), so it can be kept.
