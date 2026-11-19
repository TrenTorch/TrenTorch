__global__ void dot_partials(const float* A, const float* B, float* partial, int N) {
    extern __shared__ float s[];
    // TODO: grid-stride loop with a private accumulator, then a block tree reduction.
}

__global__ void dot_final(const float* partial, float* out, int blocks) {
    extern __shared__ float s[];
    // TODO
}
