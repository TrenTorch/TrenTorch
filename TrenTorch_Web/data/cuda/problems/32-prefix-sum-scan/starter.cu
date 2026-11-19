__global__ void scan_blocks(const float* x, float* y, float* sums, int n) {
    extern __shared__ float s[];
    // TODO: block-level inclusive scan (Hillis-Steele or Blelloch); thread blockDim.x-1 writes sums[blockIdx.x].
}

__global__ void scan_sums(float* sums, int nb) {
    // TODO: inclusive scan of the block totals, in place, with one block.
}

__global__ void add_offsets(float* y, const float* sums, int n) {
    // TODO
}
