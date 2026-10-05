---
name: data-storage-binary-search
title: 'Binary Search & Sorted Indexes'
tags: [data-structures, searching]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`01-hash-tables` finds one exact key fast. It cannot answer "every price between 10 and 20" or "the first order after noon", because hashing scatters neighbours. For range questions the data is kept **sorted**, and a sorted array can be searched by halving: look at the middle, discard the half that cannot contain the answer, repeat. Finding a position among a million sorted values takes about twenty comparisons. A sorted list of keys with positions attached is the simplest database index, and the two boundary searches built here, lower bound and upper bound, are what every range query reduces to.

### From theory to code

Implement `lower_bound(a, x)`, the first position where `x` could be inserted without breaking the order, then `upper_bound(a, x)`, the position just after the last equal value, then `range_query(a, low, high)`, every value between two limits, then `insert_sorted(a, x)`, which keeps a list sorted as new values arrive. The signatures and docstrings are already in the editor.

### Constraints

- `a` is a list of numbers sorted in non-decreasing order. Duplicates are allowed. Do not use the `bisect` module or `list.index`, and do not sort or scan the whole list for a search.
- `lower_bound(a, x)` returns the smallest index `i` such that every value before `i` is `< x`. It equals `len(a)` when all values are smaller than `x`.
- `upper_bound(a, x)` returns the smallest index `i` such that every value before `i` is `<= x`. It equals `len(a)` when all values are `<= x`.
- `range_query(a, low, high)` returns the list of values `v` with `low <= v <= high`, in order, using the two bounds above and one slice.
- `insert_sorted(a, x)` returns a **new** list with `x` inserted so the result is sorted. If equal values exist, `x` goes after them. `a` must not be modified.
- Each search must take `O(log n)` comparisons. Tests count the comparisons.

### Hints

<details>
<summary>Hint 1</summary>

Keep two indices, `low` and `high`, around the answer and look at the middle one. If it is too small the answer is to its right, otherwise it is at the middle or to its left.

</details>

<details>
<summary>Hint 2</summary>

Lower bound and upper bound differ only in whether the middle value counts as "too small" when it equals `x`. Write one and change a single comparison for the other.

</details>

<details>
<summary>Hint 3</summary>

A range of values `[low, high]` starts at `lower_bound(low)` and ends just before `upper_bound(high)`.

</details>

## Theory

### The simple version

Finding a word in a dictionary, you do not read from page one. You open near the middle, see whether your word comes before or after, and keep only that half. After a handful of openings you are on the right page. Binary search is that: every look cuts the remaining pages in half, so a million pages need only twenty looks.

### The formula

For a sorted array $a_0 \le a_1 \le \dots \le a_{n-1}$:

$$
\text{lower\_bound}(x) = \min\{\,i : a_i \ge x\,\}, \qquad \text{upper\_bound}(x) = \min\{\,i : a_i > x\,\}
$$

(with $n$ if no such $i$ exists). The count of values equal to $x$ is $\text{upper\_bound}(x) - \text{lower\_bound}(x)$, and the values in $[l, h]$ are the slice

$$
a[\,\text{lower\_bound}(l)\ :\ \text{upper\_bound}(h)\,]
$$

Each step halves the search interval, so the number of comparisons is at most

$$
\lceil \log_2 (n + 1) \rceil
$$

- The invariant: every index before `low` holds a value that is too small, and every index from `high` on holds a value that is not.
- Inserting into a sorted Python list costs $O(n)$ for the shift even though finding the position costs $O(\log n)$, which is why large indexes use trees instead of flat arrays.

### Off-by-one errors

Binary search is famous for being easy to describe and easy to get wrong. Using a half-open interval `[low, high)` and always moving to `mid + 1` or `mid` (never `mid - 1`) avoids the classic infinite loop and the missed-element bug.

### Hash index versus sorted index

A hash table finds an exact key in constant time and answers nothing about order. A sorted index takes logarithmic time but supports ranges, minimum and maximum, sorted output and prefix searches. Databases keep both kinds for this reason.

### How NumPy/PyTorch actually implements this

`bisect.bisect_left` and `bisect.bisect_right` are lower and upper bound, and `bisect.insort` inserts in place. `np.searchsorted(a, x, side='left')` and `side='right'` are the same two functions vectorized over many queries. `pandas.Index.get_loc` and `pandas.Series.searchsorted` use them on sorted indexes, and `torch.searchsorted` does the same on tensors.

## Explanation

`lower_bound` keeps the invariant that everything before `low` is smaller than `x` and everything from `high` on is not, and looks at the midpoint of the half-open interval: if the middle value is smaller than `x` the answer lies strictly to its right, otherwise the middle could still be the answer, so it becomes the new `high`. When the interval is empty, `low` is the answer. `upper_bound` is identical except that a middle value equal to `x` also counts as too small, so the search runs past the equal values. `range_query` finds the two bounds and takes one slice. `insert_sorted` uses `upper_bound` to place the new value after any equals and builds a new list around that position.
