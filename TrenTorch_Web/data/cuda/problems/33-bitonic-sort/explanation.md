### Network
For `k=2,4,...,P` and `j=k/2,...,1`, each lane compares its element with partner `i ^ j`; direction depends on the stage. Use a compare-exchange so one lane writes the lower and the other the higher value.

### CUDA considerations
- Pad to `P=next_power_of_two(N)` with a sentinel larger than all valid keys for ascending order; carry original indices if stable ordering is required.
- A single-block network can use shared memory and barriers but is limited by block size.
- Larger arrays require multi-stage global-memory passes or a hierarchical design.
- The network has `O(N log²N)` comparisons, so it is generally not the best large-scale general-purpose sort. It is useful for small fixed-size batches and predictable control flow.
