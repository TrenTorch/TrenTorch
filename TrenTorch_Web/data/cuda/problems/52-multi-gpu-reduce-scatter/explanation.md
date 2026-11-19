### What happens

**ReduceScatter** is the first half of a ring AllReduce: the ranks sum their vectors, but instead of every rank keeping the whole sum, each rank keeps only **its own shard** of it. (AllReduce is then ReduceScatter followed by AllGather, which is exactly how the ring algorithm works.)

Each rank sends and receives $\frac{P-1}{P}$ of its data, so the traffic per rank is about $B$ bytes whatever the number of GPUs.

### Memory-bound or compute-bound?

The only arithmetic is one addition per element per hop, so the operation is **bandwidth-bound** on the interconnect. Its practical value is memory: sharded optimizers and gradients (ZeRO, FSDP) use ReduceScatter so that no rank ever stores the full summed gradient.

### Pitfalls

- `recvcount` is the size of one shard; the send buffer must hold $P \times$ `recvcount` elements.
- Rank $k$ always receives shard $k$ of the sum, so the shard boundaries must line up with how your data is laid out.
