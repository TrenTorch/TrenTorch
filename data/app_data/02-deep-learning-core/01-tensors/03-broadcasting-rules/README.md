---
name: dl-core-broadcasting-rules
title: Broadcasting rules
tags: [deep-learning, tensors]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`02-elementwise-ops`'s functions all quietly relied on something never actually explained: adding a scalar to an array, or combining two differently-shaped arrays, just worked. That "just works" is called broadcasting, and it isn't magic, it's a precise rule about which shapes are allowed to combine and what shape the result gets. Without knowing the rule exactly, you can't predict when two mismatched shapes will silently combine (possibly computing something you didn't intend) versus when they'll correctly raise an error, and that unpredictability is exactly where subtle shape bugs come from later in this curriculum.

### From theory to code

Implement `broadcast_shapes(shape_a, shape_b)`, returning the shape two arrays of those shapes would broadcast to, or `None` if they're incompatible. Theory's alignment-from-the-right-then-compare-pairwise procedure maps directly onto the function: pad the shorter shape, then walk both shapes together checking one compatibility condition per dimension.

### Constraints

- Shapes are aligned starting from the trailing (rightmost) dimension; the shorter shape is conceptually padded with `1`s on the left, not the right.
- Two aligned dimensions are compatible if they're equal, or if either one is exactly `1`.
- The result dimension for a compatible pair is `max(dim_a, dim_b)`.
- If any aligned pair is incompatible, return `None` immediately — there's no such thing as a partial broadcast.
- Must handle shapes of different lengths (including a `()` scalar shape) and shapes of equal length.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

"Aligned from the right" means the last dimension of `shape_a` pairs with the last dimension of `shape_b`, the second-to-last with the second-to-last, and so on. Before you can `zip` two shapes together pairwise, you need them to be the same length — how would you make the shorter one longer without changing what it means?

</details>

<details>
<summary>Hint 2</summary>

Padding must happen on the left: `(1,) * len_diff + tuple(shorter_shape)`. Padding on the right would silently misalign every dimension in the shorter shape against the wrong dimension in the longer one.

</details>

## Theory

### The simple version

Imagine lining up two rulers by their right edges instead of their left edges, so their tick marks past a certain point compare directly even if one ruler is shorter. Any tick where one ruler simply has no mark (it ran out on the left) is treated as if it said "1," meaning "stretch to match whatever the other ruler says here." Two ticks only clash if both rulers have a real, different, non-1 number at that position.

### The formula

```text
shape_a = (8, 1, 6, 1)
shape_b =    (7, 1, 5)     # padded to (1, 7, 1, 5) to align lengths
             ↓ compare each aligned pair: equal, or either is 1
result  = (8, 7, 6, 5)
```

For each aligned pair `(dim_a, dim_b)`: compatible if `dim_a == dim_b or dim_a == 1 or dim_b == 1`, contributing `max(dim_a, dim_b)` to the result. Any incompatible pair means the whole shape pair returns `None`.

### How PyTorch actually implements this

`torch.broadcast_shapes(shape_a, shape_b)` is the real PyTorch function this mirrors, and every elementwise PyTorch op (`+`, `torch.add`, etc.) applies this exact rule internally to decide the output shape of two differently-shaped tensors before computing anything. `tests.py` has no baked PyTorch-generated numeric oracle here since this question is purely about shapes, not values, so nothing beyond this general rule is claimed.

## Explanation

`broadcast_shapes` pads whichever shape is shorter with `1`s on the _left_: `len_diff = len(shape_a) - len(shape_b)` decides which shape is shorter, and the shorter one gets `(1,) * abs(len_diff) + tuple(shorter_shape)` prepended. This is what "align from the right" means concretely, the trailing dimensions of both shapes end up compared against each other regardless of how many leading dimensions either shape originally had — `test_padding_is_on_the_left_not_the_right` exists specifically to catch an implementation that pads on the wrong side.

Then it walks the two (now equal-length) shapes pairwise with `zip(shape_a, shape_b)`, checking `dim_a == dim_b or dim_a == 1 or dim_b == 1` for each pair, exactly the compatibility rule Theory states, and appending `max(dim_a, dim_b)` to `result` whenever a pair passes. The moment any pair fails that check, the function `return`s `None` immediately, there's no way to "partially" broadcast two shapes, one incompatible dimension pair makes the whole operation invalid, which is what `test_incompatible_trailing_dims_returns_none` and `test_incompatible_matrix_shapes_returns_none` check.
