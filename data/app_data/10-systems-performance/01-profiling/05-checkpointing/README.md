---
name: systems-perf-checkpointing
title: 'Checkpointing: Save/Load Parameters to Disk, Resume Training'
tags: [mlops, profiling]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Training a real model can take hours or days — a crash, a preemption, or simply wanting to pause and resume later all mean the same thing: the current state of training (every parameter's current value, plus which epoch training had reached) needs to survive being written to disk and read back later, exactly.

### From theory to code

Implement `save_checkpoint(params, epoch, path)` and `load_checkpoint(path)`, a matched pair that write a model's parameters and its epoch number to a single file, and read them back exactly.

### Constraints

- `params`: a dict mapping parameter names (strings) to NumPy arrays of any shape/dtype.
- `path`: expected to already end in `.npz`.
- `save_checkpoint` writes every named array plus the `epoch` integer to one file at `path`.
- `load_checkpoint(path)` returns `(params, epoch)`: `params` has exactly the same name→array mapping that was saved, `epoch` is a plain Python `int`.
- A round trip (`load_checkpoint(path)` immediately after `save_checkpoint(params, epoch, path)`) must reproduce `params` and `epoch` exactly.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.savez(path, **params)` saves every dict entry as its own named array in one file — dict-unpacking with `**` turns `{"w": arr}` into the keyword argument `w=arr` automatically.

</details>

<details>
<summary>Hint 2</summary>

Save the epoch under a key that could never collide with a real parameter name (like `"__epoch__"`), so `load_checkpoint` can tell "this one's the epoch" apart from "this one's a parameter" just by its key.

</details>

## Theory

### The simple version

A checkpoint is a snapshot: freeze every number the model currently holds, plus a note saying "this is what things looked like after epoch N," and write the whole thing to one file. Loading a checkpoint is just unfreezing that snapshot later — the model (and the training loop) picks up exactly where it left off, as if no time had passed.

### The formula

```text
save_checkpoint(params, epoch, path):
    write every (name, array) pair in params, plus epoch, to one file at path

load_checkpoint(path):
    read that file back
    return (params_dict, epoch_int)
```

### How PyTorch actually implements this

Context only, untested by your submission: `torch.save(state_dict, path)` and `torch.load(path)` are PyTorch's own equivalent, typically saving a dict that includes `model.state_dict()` (parameter name → tensor, exactly this exercise's `params`), `optimizer.state_dict()` (so optimizer momentum/moment estimates also survive a restart), and the current epoch — a real training resume needs all three, not just the model weights alone, or the optimizer would restart "cold" even though the model itself picked up mid-training.

## Explanation

`save_checkpoint` calls `np.savez(path, __epoch__=np.array(epoch), **params)` — `**params` unpacks the dict into individual keyword arguments, so `np.savez` saves each parameter under its own real name inside the archive, alongside `epoch` under the reserved `__epoch__` key that can't collide with any real parameter name.

`load_checkpoint` opens the archive with `np.load(path)` and iterates its `.files` attribute (the list of every array name actually stored inside), rebuilding the `params` dict from every key except `__epoch__`, and converts that one special key's `0`-d array back to a plain Python `int` with `int(...)` — `np.load`'s own lazy-loading `NpzFile` object is used as a context manager (`with np.load(path) as data:`) so the underlying file handle is properly closed once everything needed has been read out of it.
