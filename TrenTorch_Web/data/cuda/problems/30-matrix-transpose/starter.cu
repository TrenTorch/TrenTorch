__global__ void transpose(const float* A, float* B, int H, int W) {
    // TODO: load a 32x32 tile coalesced, __syncthreads(), then write it out transposed, also coalesced.
}
