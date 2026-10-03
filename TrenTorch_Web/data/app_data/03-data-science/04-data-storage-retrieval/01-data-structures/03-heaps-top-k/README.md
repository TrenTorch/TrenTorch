---
name: data-storage-heaps-top-k
title: 'Heaps & Top-K'
tags: [data-structures, heaps]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`02-binary-search` keeps a whole array sorted so any range can be found fast. Often only the extreme is needed: the smallest pending task, the ten highest-scoring results out of ten million, the next event in a simulation. Sorting everything to read off the top wastes almost all of the work. A **heap** keeps just enough order to hand back the minimum instantly and to absorb new values cheaply. It is an ordinary array with a rule about parents and children, and it is behind priority queues, top-k selection and merging many sorted lists. This question builds the heap, and two classic uses of it.

### From theory to code

Implement the class `MinHeap` with `push(x)`, `pop()`, `peek()` and `__len__()`, then `heapify(values)`, which builds a heap from a list in linear time, then `top_k(stream, k)`, the `k` largest values of a stream using memory for only `k`, then `merge_sorted(lists)`, which merges several sorted lists into one. The skeleton and docstrings are already in the editor.

### Constraints

- `MinHeap` stores its items in a plain list `self.items` laid out as a **binary heap**: the children of index `i` are `2*i + 1` and `2*i + 2`, and every parent is `<=` both of its children. Do not use the `heapq` module.
- `push(x)` appends `x` and moves it up while it is smaller than its parent. `pop()` removes and returns the smallest item by moving the last item to the root and moving it down toward the smaller child. `peek()` returns the smallest without removing it. `pop` and `peek` on an empty heap raise `IndexError`.
- `heapify(values)` returns a new `MinHeap` containing all `values` built by sifting down from the last parent to the root, not by `n` separate pushes. `values` must not be modified.
- `top_k(stream, k)` consumes an iterable once and returns the `k` largest values as a list in **descending** order, keeping a `MinHeap` of at most `k` items. It returns fewer than `k` values if the stream is shorter, and `[]` for `k <= 0`.
- `merge_sorted(lists)` takes a list of sorted lists and returns one sorted list of all their values, using a heap that holds at most one entry per input list. Ties keep the order of the lists. It must not sort the combined list.

### Hints

<details>
<summary>Hint 1</summary>

A heap is not sorted. Only parents are no larger than their children, which is enough to find the minimum at the root and cheap enough to restore after a change, in at most the height of the tree, about `log2 n` swaps.

</details>

<details>
<summary>Hint 2</summary>

To keep the `k` largest, keep a min-heap of the best `k` seen so far. A new value only matters if it beats the smallest of those, and the smallest is exactly what the root gives you.

</details>

<details>
<summary>Hint 3</summary>

To merge, put the first value of every list into the heap, tagged with which list it came from. Pop the smallest, output it, and push the next value from the same list.

</details>

## Theory

### The simple version

A hospital emergency room does not keep patients in a fully sorted list. It only needs to know who is the most urgent right now, and to fit in new arrivals. A heap is that waiting room: the most urgent case is always at the front, adding a patient or calling the next one takes a handful of comparisons, and nobody bothers ordering the rest of the queue until their turn comes.

### The formula

Store a binary tree in an array, with the children of index $i$ at

$$
2i + 1 \quad\text{and}\quad 2i + 2, \qquad \text{parent}(i) = \left\lfloor \frac{i - 1}{2} \right\rfloor
$$

The **min-heap property** says every item is at most its children, so the smallest item is at index $0$.

- **Push** appends at the end and **sifts up** by swapping with the parent while smaller. At most $\lfloor \log_2 n \rfloor$ swaps: $O(\log n)$.
- **Pop** takes the root, moves the last item to the root and **sifts down** by swapping with the smaller child while larger. $O(\log n)$.
- **Heapify** sifts down every parent from the last one to the root. Most nodes are near the bottom and move almost nowhere, so the total cost is $O(n)$, not $O(n \log n)$.
- **Top-$k$** of $n$ items costs $O(n \log k)$ time and $O(k)$ memory, against $O(n \log n)$ time and $O(n)$ memory for sorting everything.
- **Merging** $m$ sorted lists with $N$ values in total costs $O(N \log m)$.

### Max-heaps & priorities

A max-heap flips the comparison. Libraries usually provide only a min-heap, and a max-heap is made by storing negated values. To prioritize non-numbers, store pairs `(priority, item)`, since pairs compare by their first element.

### Where this shows up

Priority queues schedule tasks, run Dijkstra's shortest-path algorithm and drive discrete-event simulations. Top-$k$ selection picks the best predictions, the largest gradients in sparsification and the most frequent items in a stream. Beam search in language models keeps a heap of the best partial sequences. External sorting and database merges use $k$-way merging.

### How NumPy/PyTorch actually implements this

The `heapq` module provides `heappush`, `heappop`, `heapify`, `nlargest`, `nsmallest` and `merge`, all on plain lists. `queue.PriorityQueue` is a thread-safe wrapper. `torch.topk` and `np.argpartition` select the top `k` of an array without a full sort. `sortedcontainers` offers sorted containers when every item must stay ordered.

## Explanation

`MinHeap.push` appends and calls `_sift_up`, which swaps the item with its parent while it is smaller. `pop` saves the root, moves the last item into the root slot, shrinks the list and calls `_sift_down`, which swaps the item with its smaller child while it is larger than that child. `heapify` copies the values into a heap's item list and sifts down every index from the last parent (`n // 2 - 1`) back to zero, which is a single linear pass. `top_k` pushes each value while there are fewer than `k` items and otherwise replaces the root when the new value is larger, then pops everything and reverses to give descending order. `merge_sorted` seeds the heap with `(value, list_index, position)` triples, so ties between equal values are broken by list order, pops the smallest and pushes the successor from the same list.
