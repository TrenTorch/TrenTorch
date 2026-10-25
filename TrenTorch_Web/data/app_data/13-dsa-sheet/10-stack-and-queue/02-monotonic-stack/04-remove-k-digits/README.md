---
name: sheet-remove-k-digits
title: 'Remove K Digits'
tags: [dsa-sheet, stack-and-queue, monotonic-stack]
difficulty: Advanced
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

**Explanation:** The greedy process keeps digits that are not larger than following digits, removing three digits from 1432219 gives "1219", the smallest possible.

**Example 2**

Input:

```python
remove_k_digits('10200', 1)
```

Output:

```text
'200'
```

**Explanation:** Removing one digit from 10200 yields "200" after discarding leading zeros, which is the minimal number achievable.

### Constraints

- `0 <= len(num) <= 200000`
- `0 <= k <= len(num)`
- `num` has no leading zeros except the number `0` itself.

## Theory

A **stack** is last in, first out: you only add (`push`) and remove (`pop`) at the top. In Python a list does this with `append()` and `pop()`, both `O(1)`.

To make a number small, the **leftmost digits matter most**. Scanning left to right, if a digit is **bigger than the digit after it**, removing the bigger one makes the number smaller (`1432` becomes `132` by removing the `4`, better than `142`). So keep a stack of digits, and before pushing a new digit, **pop while the top is bigger than the new digit and you still have removals left**.

If the digits are already non-decreasing (`1234`), removals left over are taken from the **end**. Finally strip leading zeros. `O(n)`.

This is a **greedy** choice that the stack makes cheap: a smaller digit placed earlier beats any later change.

## Explanation

The stack stays non-decreasing as long as removals remain. `stack[:len(stack) - k]` removes the leftover from the end. `lstrip("0")` drops leading zeros and `or "0"` handles an empty result.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line    | Variables                             |
| ------------------ | ------------------------------------- |
| `stack = []`       | `stack = []`                          |
| `for ch in num:`   | `stack = ['1'], ch = '4'`             |
| `stack.pop()`      | `ch = '3'`                            |
| `for ch in num:`   | `k = 2, stack = ['1', '3'], ch = '2'` |
| `k -= 1`           | `k = 1, stack = ['1']`                |
| `for ch in num:`   | `stack = ['1', '2', '2'], ch = '1'`   |
| `stack.append(ch)` | `k = 0, stack = ['1', '2', '1']`      |
| `return`           | `returned = '1219'`                   |
