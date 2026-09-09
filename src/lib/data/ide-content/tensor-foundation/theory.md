# Theory: Tensors

## What

A tensor is just an n-dimensional array with a fixed dtype -- a scalar is a 0-d tensor, a vector is 1-d, a matrix is 2-d, a batch of RGB images is 4-d. Everything a neural network computes (weights, activations, gradients, the input data itself) is stored and moved around as a tensor.

## Why not just use NumPy arrays directly

You could. In fact this `Tensor` class is a thin wrapper around exactly that -- `self.data` is a NumPy array. What a real deep learning framework's tensor adds on top is the part this specific question doesn't touch yet: autograd. Every operation on a real `torch.Tensor` also records how to compute its gradient, so that calling `.backward()` later can walk back through every operation that produced a value. That bookkeeping is what turns "a NumPy array" into "a tensor" in the deep-learning sense -- covered in the Autograd track later in this curriculum.

## How it maps onto real PyTorch

Every method here has a direct PyTorch counterpart: `tensor.add(other)` / `tensor + other`, `tensor.matmul(other)` / `tensor @ other`, `tensor.reshape(*shape)`, `tensor.transpose(*dims)`, `tensor.sum(dim=None, keepdim=False)`. The names and signatures are deliberately identical -- once you've built this, reading PyTorch's own tensor method signatures should feel immediately familiar rather than foreign.

## When each operation matters

- `add`/`sub`/`mul` are the building blocks of every loss function and every weight update.
- `matmul` is what a `Linear` layer actually is under the hood: `x @ W.T + b`.
- `reshape` shows up constantly at the seams between layers -- flattening a convolution's output before a `Linear` layer, for instance.
- `transpose` matters most in attention (later in this curriculum), where you transpose the key tensor before multiplying it against the query tensor.
- `sum` (and reductions generally) is how a loss function collapses a batch of per-example errors into the single scalar `.backward()` needs.

## Pros and cons of this NumPy-backed approach

- **Pros:** every operation is transparent -- you can read exactly what `matmul` does, with no hidden C++/CUDA kernel to trust blindly. That transparency is the whole point of building TrenTorch from scratch.
- **Cons:** it's slow and CPU-only. Real PyTorch dispatches these same operations to hand-optimized, often GPU-resident kernels (cuBLAS for matmul, for instance) that are orders of magnitude faster than this NumPy version -- correctness first, performance later is the deliberate tradeoff this curriculum makes.

## At scale

`matmul` is the operation that dominates a real network's runtime -- a single Transformer layer's attention and feedforward blocks are almost entirely matrix multiplies. The reason GPUs exist for deep learning at all is that matmul parallelizes extremely well across thousands of cores; the `np.matmul` call here computes the exact same mathematical result a GPU kernel would, just without the parallelism.
