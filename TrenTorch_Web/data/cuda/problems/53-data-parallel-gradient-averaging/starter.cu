#include <cuda_runtime.h>
#include <nccl.h>
#include <cstdio>

__global__ void fill_grad(float* g, int n, float v) {     // stands in for the backward pass
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) g[i] = v;
}

__global__ void scale_grad(float* g, int n, float factor) {
    // TODO: g[i] *= factor
}

int main() {
    const int P = 4;        // GPUs
    const int n = 8;        // gradient length
    ncclComm_t comms[4];
    ncclCommInitAll(comms, P);

    float *d_grad[4];
    float *d_sum[4];
    for (int r = 0; r < P; r++) {
        cudaSetDevice(r);
        cudaMalloc(&d_grad[r], n * sizeof(float));
        cudaMalloc(&d_sum[r], n * sizeof(float));
        fill_grad<<<1, 256>>>(d_grad[r], n, r + 1.0f);     // local gradient of rank r
    }

    // TODO 1: sum the gradients of all ranks into d_sum (ncclAllReduce).
    // TODO 2: on every rank, launch scale_grad to multiply d_sum by 1 / P.

    float h_out[8];
    for (int r = 0; r < P; r++) {
        cudaSetDevice(r);
        cudaMemcpy(h_out, d_sum[r], n * sizeof(float), cudaMemcpyDeviceToHost);
        printf("rank %d: %f\n", r, h_out[0]);
    }
    return 0;
}
