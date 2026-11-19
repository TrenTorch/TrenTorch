__global__ void cos_partials(const float* A, const float* B, float* partial, int N) {
    extern __shared__ float s[];   // s[0..255] dot, s[256..511] aa, s[512..767] bb
    // TODO
}

__global__ void cos_final(const float* partial, float* out, int blocks) {
    extern __shared__ float s[];   // 3 * 32 floats
    // TODO: sum the triples, then out[0] = dot / (sqrt(aa) * sqrt(bb)).
}
