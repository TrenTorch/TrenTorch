### Bug
```cpp
if (threadIdx.x < valid_count) {
    shared[threadIdx.x] = value;
    __syncthreads(); // unsafe if not every block thread enters
}
```

### Fix
```cpp
if (threadIdx.x < valid_count)
    shared[threadIdx.x] = value;
else
    shared[threadIdx.x] = identity;
__syncthreads();
```
All threads in the block reach the barrier. Use neutral values for inactive lanes so the later reduction remains correct.

### Rule
A block-wide barrier must be reached consistently by all threads in the block. Do not return early from some threads before a later `__syncthreads()` that other threads execute.
