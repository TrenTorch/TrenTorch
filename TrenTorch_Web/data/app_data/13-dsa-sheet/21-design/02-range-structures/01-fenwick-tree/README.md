---
name: sheet-fenwick-tree
title: 'Fenwick Tree (Prefix Sums With Updates)'
tags: [dsa-sheet, design, range-structures]
difficulty: Advanced
---

## Statement

In a **design** question you build a small data structure and run a list of operations on it. The operations are given as text, one per string, and you return the answers of the operations that produce one. Think about which operations must be fast and choose the data structure for them.

`nums` is a list of numbers. Operations: `"set i v"` changes `nums[i]` to `v`; `"sum l r"` asks for the **sum of `nums[l..r]`** (both ends included). Return the results of all `sum` operations.

For `nums = [1, 2, 3, 4]` and `["sum 0 3", "set 1 10", "sum 0 2", "sum 1 1"]` the answer is `[10, 14, 10]`.

The starter code adds up the range for each query. It is correct but too slow for big lists.

### Examples

**Example 1**

Input:

```python
run_fenwick([1, 2, 3, 4], ['sum 0 3', 'set 1 10', 'sum 0 2', 'sum 1 1'])
```

Output:

```text
[10, 14, 10]
```

**Explanation:** The first sum computes 1+2+3+4=10. After setting index 1 to 10, the sum 0..2 is 1+10+3=14, and the single element sum 1..1 is the updated value 10.

**Example 2**

Input:

```python
run_fenwick([5], ['sum 0 0', 'set 0 -5', 'sum 0 0'])
```

Output:

```text
[5, -5]
```

**Explanation:** The single element array starts with 5; summing gives 5. Setting it to -5 changes the only value, so the following sum returns -5.

### Constraints

- `1 <= len(nums) <= 100000`
- `0 <= len(ops) <= 100000`
- `-1000 <= value <= 1000`

## Theory

In a **design** question you build a small data structure and run a list of operations on it. The operations are given as text, one per string, and you return the answers of the operations that produce one. Think about which operations must be fast and choose the data structure for them.

A prefix-sum array answers a range sum in `O(1)` but an update forces you to rewrite `O(n)` prefixes. A **Fenwick tree** (binary indexed tree) balances both: update and prefix sum cost `O(log n)`.

The tree is an array `tree[1..n]` where `tree[i]` stores the sum of a block of `lowbit(i) = i & -i` elements ending at `i`. To get the prefix sum up to `i`, add `tree[i]`, then `i -= i & -i` (jump to the next block on the left), until `i = 0`. To add `delta` at position `i`, add it to `tree[i]`, then `i += i & -i` (the next block that contains this position), until `i > n`.

A range sum is `prefix(r) - prefix(l - 1)`; a `set` is an `add` of the difference to the old value. This uses the `n & -n` trick from the bit manipulation topic.

## Explanation

`add` and `prefix` walk the blocks with `i & -i`. `values` remembers the current numbers so `set` can compute the difference.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                | Variables                                                                                                                                                                               |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `n = len(nums)`                | `n = 4`                                                                                                                                                                                 |
| `def prefix(i):`               | `tree = [0, 0, 0, 0, 0], values = [1, 2, 3, 4], add = <function run_fenwick.<locals>.add at 0x000001F48554E7A0>, prefix = <function run_fenwick.<locals>.prefix at 0x000001F48554D900>` |
| `for i, x in enumerate(nums):` | `tree = [0, 1, 3, 0, 3], i = 2, x = 3`                                                                                                                                                  |
| `out = []`                     | `tree = [0, 1, 3, 3, 10], i = 3, x = 4, out = []`                                                                                                                                       |
| `for op in ops:`               | `out = [10], op = 'set 1 10', parts = ['sum', '0', '3'], left = 0, right = 3`                                                                                                           |
| `values[i] = v`                | `tree = [0, 1, 11, 3, 18], values = [1, 10, 3, 4], i = 1, parts = ['set', '1', '10'], v = 10`                                                                                           |
| `for op in ops:`               | `out = [10, 14], op = 'sum 1 1', parts = ['sum', '0', '2'], right = 2`                                                                                                                  |
| `return`                       | `returned = [10, 14, 10]`                                                                                                                                                               |
