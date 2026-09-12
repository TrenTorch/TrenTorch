---
name: dl-training-dataset-dataloader
title: 'Dataset/DataLoader abstraction (indexing, batching, shuffling)'
tags: [neural-networks, training, data-processing]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A real training set rarely fits neatly into the shape a model's forward pass expects, delivered in exactly the right batch size, in exactly the right order, exactly once per epoch. It usually lives as a big pile of samples (rows in a CSV, image files in a folder, entries in a database), and turning that pile into a stream of correctly-shaped, correctly-shuffled batches, every single epoch, is genuinely fiddly bookkeeping: how many full batches fit, what to do with the leftover samples that don't fill a full batch, how to shuffle WITHOUT accidentally mismatching a feature with the wrong target.

Splitting this into two separate pieces, a `Dataset` (which only knows how to answer "how many samples do you have" and "give me sample number `i`") and a `DataLoader` (which only knows how to turn a `Dataset` into a stream of shuffled batches), is what lets the SAME `DataLoader` logic work for a tiny in-memory array of 100 samples and a dataset that streams gigabytes of images off disk: `DataLoader` never needs to know or care how a `Dataset` actually stores its data, only that it can answer `len(dataset)` and `dataset[i]`.

### From theory to code

Implement `ArrayDataset.__len__` and `__getitem__` (the simplest possible `Dataset`, wrapping two parallel arrays), and `DataLoader.__iter__` and `__len__`. `DataLoader.__iter__` should build an index array `[0, 1, ..., len(dataset)-1]`, shuffle it in place (using `np.random.RandomState(self.seed)` for reproducibility) if `self.shuffle` is `True`, then walk through it in chunks of `self.batch_size`, using each chunk of indices to gather and stack the corresponding samples from `self.dataset`, yielding one `(batch_features, batch_targets)` pair per chunk.

### Constraints

- `ArrayDataset.__getitem__(idx)` returns a `(feature, target)` pair for that single index, not a batch.
- `DataLoader.__iter__` must yield every sample in the dataset EXACTLY once per full iteration, the last batch may be smaller than `batch_size` if the dataset size doesn't divide evenly, but no sample is skipped or duplicated.
- When `shuffle=True`, use `np.random.RandomState(self.seed)` specifically (not the global `np.random` state), so results are reproducible given the same `seed`.
- `DataLoader.__len__` returns the number of batches a full pass produces (`ceil(len(dataset) / batch_size)`), not the number of samples.

### Hints

<details>
<summary>Hint 1: ArrayDataset</summary>

`__len__` is just `len(self.features)`; `__getitem__(idx)` is `return self.features[idx], self.targets[idx]`.

</details>

<details>
<summary>Hint 2: Building and shuffling the index array</summary>

`indices = np.arange(len(self.dataset))`, then, if `self.shuffle`, `np.random.RandomState(self.seed).shuffle(indices)` shuffles it IN PLACE (it returns `None`, not a shuffled copy).

</details>

<details>
<summary>Hint 3: Walking through in chunks</summary>

`for start in range(0, len(indices), self.batch_size):` then `batch_indices = indices[start : start + self.batch_size]` naturally gives you a shorter final slice if the total doesn't divide evenly, no special-casing needed. Gather with `np.stack([self.dataset[i][0] for i in batch_indices])` for the features (and similarly for targets), then `yield` the pair.

</details>

## Theory

### The simple version

A library's card catalog doesn't store the actual books, it stores where to FIND each book (its call number), and a librarian pulling a cart of books for a reading group only needs the call numbers, not any special knowledge of how the shelves are physically organized. `Dataset` is the catalog (answering "how many books, and here's book number `i`"), and `DataLoader` is the librarian pulling batches off the shelf, shuffled or in order, without ever needing to know anything about how the books themselves are stored.

### The formula

There's no numeric formula here; this is a data-flow / iteration-protocol exercise. The one arithmetic detail worth stating explicitly is how many batches a full pass produces:

```
num_batches = ceil(len(dataset) / batch_size)
            = (len(dataset) + batch_size - 1) // batch_size
```

(integer-division form of ceiling division, avoiding floating point).

### How PyTorch actually implements this

`torch.utils.data.Dataset` is exactly this abstract contract: subclasses implement `__len__` and `__getitem__`, and nothing else is required. `torch.utils.data.DataLoader` implements the same batching and shuffling logic built here, plus significant extra machinery this question deliberately leaves out for simplicity: `num_workers` spins up separate OS processes to prefetch and preprocess batches in parallel with the GPU actually training on the PREVIOUS batch (so the GPU is rarely left waiting on data loading), and `collate_fn` lets you customize exactly how a list of individual samples gets stacked into a batch (needed, for instance, when samples have variable length, like sentences of different lengths in NLP, and need padding before they can be stacked into one tensor). `[02-assemble-training-loop]`, immediately next in this track, is where this `DataLoader` gets used for real: `for batch_x, batch_y in loader:` is the very first line of essentially every PyTorch training loop ever written.

## Explanation

`ArrayDataset.__len__` returns `len(self.features)`, and `__getitem__(idx)` returns the matching `(features[idx], targets[idx])` pair, satisfying the minimal `Dataset` contract `DataLoader` relies on.

`DataLoader.__iter__` builds `indices = np.arange(len(self.dataset))`, optionally shuffles it in place with a seeded `RandomState` for reproducibility, then loops over `range(0, len(indices), self.batch_size)`, slicing out each chunk of indices, gathering and stacking the corresponding samples via list comprehensions over `self.dataset[i]`, and yielding each `(batch_features, batch_targets)` pair. `__len__` computes the ceiling-division batch count directly, `(len(dataset) + batch_size - 1) // batch_size`, without needing to actually iterate.
