### Kernel
```cpp
__global__ void tanh_kernel(const float* X, float* Y, int N) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < N) Y[i] = tanhf(X[i]);
}
```

### Analysis
The map is independent per element. Math-function throughput and memory traffic jointly determine performance. Compare `tanhf` with any faster intrinsic or algebraic formulation only under a stated tolerance. The identity based on exponentials can overflow for large magnitudes and is not automatically a better implementation.
