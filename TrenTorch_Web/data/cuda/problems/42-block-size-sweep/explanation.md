### Task
Benchmark a representative kernel with block sizes such as 64, 128, 256, and 512 threads (where legal and sensible). Keep the input, GPU clocks/power state, compiler flags, and measurement method controlled.

### Report
Record:
- Kernel time and effective bandwidth/FLOP rate.
- Registers per thread and shared memory per block.
- Theoretical and achieved occupancy.
- Memory throughput and relevant stall reasons.
- Number of blocks and tail effects.

### Interpretation
More threads per block do not automatically mean higher occupancy or throughput. Larger blocks may reduce scheduling overhead but increase resource allocation granularity. Small workloads may be launch-bound, making block-size differences noisy. Choose the block size based on repeated measurements and profiler evidence, not a universal rule.
