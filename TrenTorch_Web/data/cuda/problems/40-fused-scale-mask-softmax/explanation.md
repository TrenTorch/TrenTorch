### Algorithm
1. Apply scale and mask while finding the row maximum.
2. Reduce the maximum.
3. Compute exponentials only for valid positions and reduce their sum.
4. Normalize and write output.
A tiled implementation can use online `(max, sum-exp)` state for long rows.

### Why fuse
Separate scale, mask, and softmax kernels materialize intermediates. Fusion avoids those writes and rereads. Ensure masked values remain excluded even when all positions in a row are masked; define the expected output for that case to avoid `-inf - -inf` NaNs.
