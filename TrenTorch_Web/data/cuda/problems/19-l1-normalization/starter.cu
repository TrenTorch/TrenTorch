__global__ void abs_sum_partials(const float* x, float* partial, int n) {
    extern __shared__ float s[];
    // TODO
}

__global__ void sum_final(const float* partial, float* out, int blocks) {
    extern __shared__ float s[];
    // TODO
}

__global__ void l1_map(const float* x, float* y, int n, const float* denom) {
    // TODO
}
