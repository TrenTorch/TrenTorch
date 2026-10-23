---
name: sheet-assign-cookies
title: 'Assign Cookies'
tags: [dsa-sheet, greedy, greedy-basics]
difficulty: Beginner
---

## Statement

Child `i` is happy with a cookie of size at least `greed[i]`. Cookie `j` has size `sizes[j]`. Each child gets **at most one** cookie and each cookie goes to **at most one** child. Return the **largest number of happy children**.

For `greed = [1, 2, 3]` and `sizes = [1, 1]` the answer is `1`.

### Examples

**Example 1**

Input:

```python
assign_cookies([1, 2, 3], [1, 1])
```

Output:

```text
1
```

**Example 2**

Input:

```python
assign_cookies([1, 2], [1, 2, 3])
```

Output:

```text
2
```

### Constraints

- `0 <= len(greed), len(sizes) <= 200000`
- `1 <= greed[i], sizes[j] <= 10**9`

## Theory

A **greedy** algorithm builds the answer step by step and, at each step, takes the choice that looks best **right now**, without ever going back. It is fast and simple, but it is only correct when the problem has a structure that makes local choices safe. The hard part is the **proof**: show that the greedy choice can always be part of some best answer.

Give each cookie to the **least greedy child it can still satisfy**. Sort both lists. Go through the children from the least greedy; for each, use the **smallest cookie** that is big enough. A bigger cookie would also work, but it might be needed by a greedier child later, so using the smallest sufficient cookie wastes nothing.

Two pointers do it in one pass after sorting: advance the cookie pointer until a cookie satisfies the current child, then move to the next child. `O(n log n)` for the sorts.

## Explanation

`child` counts the happy children. Each cookie is looked at once, in increasing size, and it satisfies the current least greedy child if it can.
