### LSD radix pass
For each digit:
1. Extract digit bits.
2. Build per-bin counts (often per block).
3. Scan counts to determine global bin offsets and per-block offsets.
4. Compute each element's stable local rank within its block/bin.
5. Scatter to the output buffer.
6. Swap input/output buffers and continue to the next digit.

### Analysis
Radix sort is data-independent and can be linear in input size for a fixed number of digit passes. It relies on histogram and scan primitives and moves the data each pass. Quicksort is comparison-based, has expected `O(N log N)` work, and can suffer from poor pivots/irregular control flow. For GPU workloads, use CUB `DeviceRadixSort` as a production baseline where allowed.

### Correctness
Define signed-key transformation, floating-point ordering (including NaNs and signed zero), stability, and key/value association. Do not claim stable sorting unless the scatter preserves input order within each digit.

---
