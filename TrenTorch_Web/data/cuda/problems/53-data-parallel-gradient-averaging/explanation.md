### What happens

In data-parallel training every GPU holds a full copy of the model and processes a different slice of the batch. After the backward pass each GPU has a **different** gradient; to keep the copies identical they must apply the **same** update, the mean gradient. So every step does an AllReduce (sum) and a division by the number of ranks. Frameworks fuse the division into the reduction (NCCL has an `ncclAvg` operation) or fold it into the learning rate; here you do it explicitly with a kernel.

### Memory-bound or compute-bound?

The two parts behave differently:

- **`scale_grad`** reads and writes each element once and does one multiplication: arithmetic intensity $\frac{1}{8}$ FLOP/byte, far below the GPU's ridge point, so it is **memory-bound**.
- **The AllReduce** does one addition per element but moves about $2\,\frac{P-1}{P}$ bytes per gradient byte over the **interconnect**, so it is **bandwidth-bound on the link**. This is why large models overlap the AllReduce with the backward pass instead of waiting for it.

### Pitfalls

- Launch the scale kernel on **every** rank, after `cudaSetDevice(r)`, or only some ranks hold the mean.
- Scaling the *inputs* instead of the sum also works; dividing twice does not.
