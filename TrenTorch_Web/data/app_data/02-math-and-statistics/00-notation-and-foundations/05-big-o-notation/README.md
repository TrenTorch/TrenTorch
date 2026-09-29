---
name: math-big-o-notation
title: 'Asymptotic Notation: Big-O for Algorithm and Memory Complexity'
tags: [notation, foundations]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

"Is this fast enough?" depends on how an algorithm's cost grows as the input grows, not on how it performs at one specific size. `O(n)` and `O(n²)` are the vocabulary for talking about that growth rate directly, independent of any particular machine's speed — and it's exactly the vocabulary the Inference track uses to reason about attention's `O(n²)` cost in sequence length, or a matrix multiply's `O(n³)` cost in dimension. This question makes the connection between "the formula says `O(n)`" and "the code actually does about `n` units of work" concrete, by counting real operations instead of trusting the formula on faith.

### From theory to code

Implement `count_comparisons_linear_search(arr, target)`, returning **both** whether `target` was found **and** how many comparisons the search made, then `count_comparisons_binary_search(sorted_arr, target)`, doing the same for binary search on a sorted array. The signatures and docstrings are already in the editor.

### Constraints

- `arr` / `sorted_arr` is a list of numbers; `sorted_arr` is guaranteed to already be sorted ascending.
- Each function returns a tuple `(found, comparisons)`, where `found` is a `bool` and `comparisons` is the count of element-to-target comparisons actually performed (not counting index bookkeeping like a loop counter).
- `count_comparisons_binary_search` must actually halve its search space each step — a linear scan disguised as a "binary search" that happens to still find the target does not count.

### Hints

<details>
<summary>Hint 1</summary>

Linear search: walk `arr` left to right, comparing each element to `target` and incrementing a counter every time, stopping (and returning `True`) the moment a match is found.

</details>

<details>
<summary>Hint 2</summary>

Binary search: maintain `lo`/`hi` bounds, look at the midpoint, count that one comparison, and narrow to one half or the other based on whether the midpoint is less than, greater than, or equal to `target` — repeat until `lo > hi`.

</details>

## Theory

### The simple version

Looking up a name in an unsorted stack of business cards means checking them one at a time until you find it — in the worst case (the name is last, or missing entirely), you check every single card. Looking up a name in a phone book (sorted, alphabetically) means opening to the middle, deciding "earlier half or later half," and repeating — each check eliminates half of what's left, so even a million-entry phone book takes at most about 20 checks, not a million.

### The formula

$$
O(g(n)) = \{ f(n) : \exists\, c > 0, n_0 \text{ such that } 0 \leq f(n) \leq c \cdot g(n) \; \forall\, n \geq n_0 \}
$$

- `f(n)` — the actual cost (time, or memory) of running the algorithm on an input of size `n`.
- `g(n)` — a simple reference function (`n`, `n²`, `log n`, ...) that `f(n)` is being compared against.
- "`f(n)` is `O(g(n))`" — informally, "for large enough `n`, `f(n)` grows no faster than a constant multiple of `g(n)`." The formal `∃ c, n₀` definition exists specifically to let you ignore constant factors and small-`n` behavior, which is why `O(n)` never mentions whether the constant is `1` operation per element or `50`.

Two complexities appear directly in this question:

- **Linear search is `O(n)`**: in the worst case, every one of the `n` elements is compared once.
- **Binary search is `O(log n)`**: each comparison eliminates half the remaining candidates, so the number of comparisons needed is the number of times `n` can be halved before reaching `1` — exactly `log₂ n`.

### Reading complexity off a piece of code directly

A single loop over `n` items, doing constant work per item, is `O(n)`. A loop nested inside another loop, each running over `n` items, is `O(n²)` — this is exactly why a naive matrix multiply (Module 7 of the NumPy track: `n × n` output entries, each needing a length-`n` dot product) is `O(n³)`, and why attention (Inference track) comparing every query against every key is `O(n²)` in sequence length. A loop that halves its remaining work each iteration, like binary search, is `O(log n)` regardless of how much work happens per iteration, as long as that per-iteration work is itself constant.

### How this shows up elsewhere on this site

Every "why is this operation slow/fast" discussion in the NumPy Performance & Memory module and the Inference track's serving-latency questions is ultimately a Big-O argument made concrete with real measurements — this question is the vocabulary those measurements get described in.

## Explanation

`count_comparisons_linear_search` walks `arr` left to right with a plain `for` loop, incrementing `comparisons` and checking equality against `target` at every single element, returning as soon as a match is found (or after the whole list, if not). `count_comparisons_binary_search` maintains `lo = 0` and `hi = len(sorted_arr) - 1`, and on each iteration computes `mid = (lo + hi) // 2`, counts exactly one comparison for that midpoint, and narrows to `sorted_arr[mid+1:hi]` or `sorted_arr[lo:mid-1]` depending on the comparison's outcome — halving the remaining range every iteration is what makes the comparison count grow logarithmically rather than linearly with input size.
