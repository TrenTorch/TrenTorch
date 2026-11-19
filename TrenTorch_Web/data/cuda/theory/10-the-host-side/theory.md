# The host side

## The standard flow

```cuda
float *d_x;
cudaMalloc(&d_x, n * sizeof(float));                      // 1. allocate on device
cudaMemcpy(d_x, h_x, n * sizeof(float), cudaMemcpyHostToDevice);  // 2. copy in
kernel<<<grid, block>>>(d_x, /* ... */, n);               // 3. launch (async)
cudaMemcpy(h_y, d_y, n * sizeof(float), cudaMemcpyDeviceToHost);  // 4. copy out (waits)
cudaFree(d_x);                                            // 5. release
```
A plain `cudaMemcpy` waits for earlier GPU work to finish, which is why the result is ready when it returns. `cudaDeviceSynchronize()` waits explicitly.

## Errors

Launches do not return errors directly. After a launch call `cudaGetLastError()`; after synchronizing, check the return codes. In this course the simulator reports out-of-bounds accesses, double frees and leaks with the exact kernel, block and thread.

## Memory discipline

Every `cudaMalloc` needs a `cudaFree`. Leaked device memory is reported in the run report.

## Interactive: Who is waiting for whom?

<div class="cuda-viz" data-viz="VIZ-HOST-TIMELINE" data-title="Who is waiting for whom?" data-spec="VIZ-HOST-TIMELINE"></div>

## Check yourself

1. After a kernel launch returns, is the output buffer ready?
2. What happens if you forget `cudaFree` in a loop of 1,000 iterations?

<details class="answers">
<summary>Show answers</summary>

1. Not necessarily: launch is async.
2. leak ⇒ out-of-memory error eventually.

</details>

## Practice

[CU-001 Vector Addition](problem:CU-001)
