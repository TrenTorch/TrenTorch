__global__ void max_partials(const float* X, float* partial, int N) {
    extern __shared__ float s[];
    // TODO
}

__global__ void max_final(const float* partial, float* out, int blocks) {
    extern __shared__ float s[];
    // TODO
}
