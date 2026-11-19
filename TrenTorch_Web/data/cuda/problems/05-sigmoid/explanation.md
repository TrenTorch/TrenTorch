### Kernel
```cpp
__global__ void sigmoid(const float* X, float* Y, int N) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < N) {
        float x = X[i];
        Y[i] = 1.0f / (1.0f + expf(-x));
    }
}
```

### Optimization and numerical notes
- `expf` prioritizes the CUDA math-library accuracy contract.
- `__expf` may be faster on some architectures but has a different accuracy contract. Benchmark and measure maximum/ULP error against the required tolerance.
- The output still requires one input read and one output write, but exponential throughput may make the kernel compute/instruction-bound rather than purely bandwidth-bound.
- Very large positive/negative inputs naturally approach 1/0; avoid algebraic rewrites unless their overflow and rounding behavior are checked.

**Best practice:** Select the math intrinsic based on the accepted error tolerance, not speed alone.
