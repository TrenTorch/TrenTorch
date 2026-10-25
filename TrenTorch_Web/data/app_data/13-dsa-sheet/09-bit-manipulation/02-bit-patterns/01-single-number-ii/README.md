---
name: sheet-single-number-ii
title: 'Single Number, Others Three Times'
tags: [dsa-sheet, bit-manipulation, bit-patterns]
difficulty: Advanced
---

## Statement

Every value in `nums` appears **exactly three times**, except one value that appears **once**. Return that value. Use `O(1)` extra memory if you can (counting with a dictionary is allowed, but the challenge is to do it without one).

### Examples

**Example 1**

Input:

```python
single_number_ii([2, 2, 3, 2])
```

Output:

```text
3
```

**Explanation:** The value 2 occurs three times and 3 occurs once, so the unique element is 3.

**Example 2**

Input:

```python
single_number_ii([0, 1, 0, 1, 0, 1, 99])
```

Output:

```text
99
```

**Explanation:** Values 0 and 1 each appear three times while 99 appears once, making 99 the single number.

### Constraints

- `1 <= len(nums) <= 300000`
- `len(nums) % 3 == 1`
- `-2**31 <= nums[i] < 2**31`

## Theory

XOR cancels pairs but not triples. The fix is to count **per bit position** (mod 3): for each of the 32 bit positions, add up that bit over all numbers. A number that appears three times contributes a multiple of 3 to every position, so only the single number leaves a remainder: the sum at that position `% 3` is the single number's bit.

A loop over the 32 positions works (`sum((x >> i) & 1 for x in nums) % 3`), but it reads the list 32 times. The same counting can be done for **all bits at once** with two numbers: `ones` holds the bits seen once (mod 3) and `twos` the bits seen twice. For each `x`: `ones = (ones ^ x) & ~twos`, then `twos = (twos ^ x) & ~ones`. A bit that is seen a third time is cleared from both, so only the single number remains in `ones`.

That is one pass, `O(n)` time and `O(1)` memory. Python integers behave like infinitely long two's complement numbers for `^`, `&` and `~`, so negative values work without special care.

## Explanation

For each bit, the number of times it is seen is a multiple of 3 for the tripled values, so only the single number's bits are left in `ones` after every value is processed.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line             | Variables            |
| --------------------------- | -------------------- |
| `ones = twos = 0`           | `ones = 0, twos = 0` |
| `for x in nums:`            | `x = 2`              |
| `ones = (ones ^ x) & ~twos` | `(no change)`        |
| `twos = (twos ^ x) & ~ones` | `twos = 2`           |
| `ones = (ones ^ x) & ~twos` | `ones = 1, x = 3`    |
| `twos = (twos ^ x) & ~ones` | `twos = 0`           |
| `ones = (ones ^ x) & ~twos` | `ones = 3, x = 2`    |
| `return`                    | `returned = 3`       |

### Complexity

- Time: O(n) where n is length of nums.
- Extra space: O(1) extra memory.
- The brute force takes O(n) where n is length of nums.
