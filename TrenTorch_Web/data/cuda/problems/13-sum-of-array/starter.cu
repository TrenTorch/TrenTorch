__global__ void sum_partials(const float* X, float* partial, int N) {
    extern __shared__ float s[];
    // TODO: load one element (or 0) into shared memory, tree-reduce, thread 0 writes partial[blockIdx.x].
}

__global__ void sum_final(const float* partial, float* out, int blocks) {
    extern __shared__ float s[];
    // TODO: reduce the `blocks` partials with one block; thread 0 writes out[0].
}
