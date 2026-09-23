---
name: potd-menu-photo-padding-1d-conv
title: 'MENU PHOTO PADDING'
tags: [computer-vision]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** Computer Vision

---

### Story

Zomato's menu-photo pipeline needs 1D-signal intuition for 2D convolution padding before the full
CNN track: implement "same" versus "valid" padding for a 1D convolution as the warm-up.

---

### The Math

**Valid:** no padding, output length `= n - k + 1`.

**Same:** pad symmetrically with zeros so output length `= n` (for odd kernel size `k`, pad
`floor(k / 2)` on each side).

### Input Format

```
n k
x_1 ... x_n
kernel_1 ... kernel_k
mode  (either "valid" or "same")
```

### Output Format

Convolution output, space-separated, 6 decimals.

### Constraints

- `1 <= k <= n <= 10^4`, `k` odd
- Time limit: 1.0 second.

---

### Example

**Input**

```
5 3
1 2 3 4 5
1 0 -1
valid
```

**Output**

```
-2.000000 -2.000000 -2.000000
```

Same input with `mode = same`:

```
-2.000000 -2.000000 -2.000000 -2.000000 4.000000
```

## Theory

### The simple version

A convolution slides a small kernel across a signal and combines nearby values. "Valid" padding only looks where the kernel fully fits; "same" padding pads the edges with zeros so the output stays the same length as the input.

### This is cross-correlation, not flipped convolution

The kernel is **not** flipped before sliding it across the signal: this is cross-correlation, the
convention every deep learning framework actually implements despite calling it "convolution." A
true (flipped-kernel) convolution implementation produces a different, mirrored answer and must be
stated against explicitly.

### "Same" pads, it does not shrink

`"same"` mode zero-pads the signal on both sides so the output length equals the input length `n`,
rather than computing a smaller output and padding that afterward. For odd `k`, the pad amount on
each side is `k // 2`.

### The boundary is genuinely zero, not wrapped or clamped

Inside `"same"` mode, a window that extends past the original signal's edge multiplies the
out-of-bounds positions by the kernel and adds zero for each of them, since the padded values are
zero. The boundary must not wrap around to the other end of the signal, and must not clamp to the
nearest real edge value; both would silently produce a different (wrong) answer only at the edges.

### `k = 1` makes both modes identical

With a kernel of size `1`, convolution degenerates to multiplying every position by the single
kernel weight; there is no window to shift, so `"valid"` and `"same"` produce the same output.

## Explanation

`conv1d` builds the signal to slide over: unchanged for `"valid"`, or zero-padded by `k // 2` on
each side for `"same"`. It then slides the kernel across that signal without flipping it, computing
`sum(window[i] * kernel[i] for i in range(k))` at each position, which is the cross-correlation
formula. For `"valid"` the number of positions is `n - k + 1` by construction (the loop only runs
where a full window fits inside the unpadded signal); for `"same"`, the padded signal is
`n + 2*(k//2)` long, giving `n + 2*(k//2) - k + 1 = n` positions when `k` is odd, exactly the input
length.
