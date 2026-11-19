__global__ void fused_scale_mask_softmax(const float* X, const int* mask, float* Y, int rows, int K, float scale) {
    __shared__ float s[128];
    // TODO: max over unmasked scale*x; sum of exp; write exp/sum, or 0 for masked / fully masked rows.
}
