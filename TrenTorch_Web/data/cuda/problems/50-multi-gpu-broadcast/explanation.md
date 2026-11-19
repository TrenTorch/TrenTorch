### What happens

A **broadcast** copies the root's buffer to every other rank. With $P$ ranks and a message of $B$ bytes, a naive implementation sends $B$ bytes $P-1$ times from the root, so the root's link is the bottleneck. NCCL arranges the ranks as a ring or a tree so that every link carries about $B$ bytes once, whatever $P$ is.

### Memory-bound or compute-bound?

There is no arithmetic at all: a broadcast is pure data movement, so its time is set by the **interconnect** (NVLink inside a node, PCIe or the network across nodes), not by the GPUs' FLOPs. The report below shows how many bytes each GPU moved over the interconnect.

### Pitfalls

- Every rank must call `ncclBroadcast` with the **same root and count**, in the same order as the other collectives. A mismatch hangs a real cluster; the simulator reports it.
- The send buffer on non-root ranks is ignored, but it must still be a valid allocation.
