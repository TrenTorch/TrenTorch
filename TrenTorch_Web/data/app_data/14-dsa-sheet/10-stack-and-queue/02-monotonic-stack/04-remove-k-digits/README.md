---
name: sheet-remove-k-digits
title: 'Remove K Digits'
tags: [dsa-sheet, stack-and-queue, monotonic-stack]
difficulty: Advanced
theory: removing-digits-to-get-a-smaller-number
---

## Statement

`num` is a non-negative number written as a string of digits. Remove exactly `k` digits so that the number left is **as small as possible**. Return it as a string without leading zeros (return `"0"` if nothing is left or only zeros are).

For `num = "1432219"` and `k = 3` the answer is `"1219"`.

### Examples

**Example 1**

Input:

```python
remove_k_digits('1432219', 3)
```

Output:

```text
'1219'
```

**Example 2**

Input:

```python
remove_k_digits('10200', 1)
```

Output:

```text
'200'
```

### Constraints

- `0 <= len(num) <= 200000`
- `0 <= k <= len(num)`
- `num` has no leading zeros except the number `0` itself.

## Explanation

The stack stays non-decreasing as long as removals remain. `stack[:len(stack) - k]` removes the leftover from the end. `lstrip("0")` drops leading zeros and `or "0"` handles an empty result.

### Complexity

- Time: O(n). Each digit is pushed once and popped at most once.
- Space: O(n). The stack.
