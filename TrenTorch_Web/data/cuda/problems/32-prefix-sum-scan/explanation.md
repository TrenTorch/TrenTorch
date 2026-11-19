### Single-block Blelloch outline
1. Load values into shared memory, padding out-of-range lanes with zero.
2. Upsweep: build subtree sums.
3. Set root to zero for exclusive scan.
4. Downsweep: propagate prefix sums.
5. Write results, converting to inclusive by adding original input if needed.

### Multi-block design
A scalable scan uses three stages:
1. Scan each block independently and write each block's total.
2. Scan the block totals.
3. Add each block's offset to its local scan output.

This avoids an unsafe cross-block barrier. For small arrays, one block is sufficient; for large arrays, multi-block overhead is worthwhile. Use a tested library primitive such as CUB when permitted; it is usually the strongest production baseline.

### Correctness
Specify inclusive/exclusive semantics, integer overflow behavior, and whether input/output may alias. Handle non-power-of-two lengths and final partial blocks.
