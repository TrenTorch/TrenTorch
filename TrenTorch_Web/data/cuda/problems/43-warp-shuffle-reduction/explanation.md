### Warp sum
```cpp
__device__ float warp_sum(float v) {
    unsigned mask = 0xffffffffu; // valid only when all 32 lanes participate
    for (int offset=16; offset>0; offset>>=1)
        v += __shfl_down_sync(mask, v, offset);
    return v;
}
```

### Correctness constraints
The mask must identify participating lanes. The simple all-ones mask is valid only when the full warp executes the intrinsic in a converged manner. For partial warps, construct a correct active mask and ensure the reduction logic accounts for inactive lanes. To reduce across a block, each warp writes one sum to shared memory, synchronize, then one warp reduces the warp sums.

### Benefit
Warp shuffles exchange register values directly between lanes, avoiding shared-memory stores/loads and a block barrier for the intra-warp phase. They do not replace synchronization needed between warps.
