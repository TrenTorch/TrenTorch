### What happens

**AllGather** concatenates every rank's shard, in rank order, and gives the whole result to every rank. It is the collective behind tensor-parallel layers: each GPU computes a slice of an activation, then an AllGather rebuilds the full activation everywhere.

With $P$ ranks and shards of $S$ bytes, a ring AllGather runs $P-1$ steps; in each step every rank forwards one shard to its neighbour, so each link carries $(P-1)\,S$ bytes in total and every rank ends up holding $P\,S$ bytes.

### Memory-bound or compute-bound?

No arithmetic: the cost is bytes over the interconnect. The receive buffer is $P$ times larger than the send buffer, so the **memory footprint** grows with the number of GPUs, which is why very wide tensor parallelism is limited by memory as well as by bandwidth.

### Pitfalls

- `sendcount` is the size of **one** shard, not of the gathered result.
- The receive buffer must hold $P \times$ `sendcount` elements, or the simulator reports an out-of-bounds write.
