---
name: lm-next-token-batches
title: Next-Token Training Windows
tags: [tokenization, data-loading, language-modeling]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A language model is trained on one enormous stream of token ids. To feed it a batch, the stream is cut into windows of fixed length `block_size`, and the target for each input window is the **same window shifted one token to the right**, because at every position the label is simply the next token. The `stride` controls overlap between consecutive windows: a stride equal to `block_size` uses every token once per epoch, a smaller stride repeats context, which gives more training examples at the cost of redundancy.

### From theory to code

Implement `make_lm_windows`.

### Constraints

- `token_ids` is a 1-D integer array of length `n`. `make_lm_windows(token_ids, block_size, stride)` returns `(X, Y)`, both of shape `(num_windows, block_size)`.
- Window `w` starts at `s = w * stride`. `X[w] = token_ids[s : s + block_size]` and `Y[w] = token_ids[s + 1 : s + block_size + 1]`.
- Only complete windows are returned: `num_windows = (n - block_size - 1) // stride + 1` when `n >= block_size + 1`, else `0` (empty arrays of shape `(0, block_size)`).
- `stride >= 1`.

### Hints

<details>
<summary>Hint 1</summary>

The last valid start index must satisfy `s + block_size + 1 <= n`, because the target reads one token past the input window.

</details>

<details>
<summary>Hint 2</summary>

Build the start indices with `np.arange(num_windows) * stride` and use fancy indexing with an offset grid.

</details>

## Theory

### The simple version

To teach a child to predict the next word, show them a short line of text and ask for the word that follows each position. Sliding that line along the book gives thousands of lessons from one story.

### The formula

$$
X_{w,t} = x_{ws + t}, \qquad Y_{w,t} = x_{ws + t + 1}, \qquad 0 \le t < B
$$

The training loss is the mean cross-entropy between the model's prediction at $(w, t)$ and $Y_{w,t}$, so one window supplies $B$ training signals at once.

### How this is done in practice

PyTorch pipelines wrap this in a `Dataset` whose `__getitem__` returns one window, often at a random start index instead of a fixed stride. Large-scale training memory-maps a pre-tokenized binary file so windows are sliced without loading the corpus.

## Explanation

The only subtlety is the off-by-one at the end: a window is usable only if its shifted target fits in the stream. Fancy indexing with a start-offset grid builds all windows in a single operation.
