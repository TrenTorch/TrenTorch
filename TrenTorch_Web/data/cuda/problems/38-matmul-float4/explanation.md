### Design
Build on CU-032. Vectorize contiguous global loads when row alignment and tile boundaries permit. Use aligned `float4` transactions for groups of four values, then distribute components to per-thread fragments. Pad shared-memory dimensions where transposed access patterns would otherwise create bank conflicts.

### Requirements
- Verify base pointers and row strides satisfy 16-byte alignment.
- Handle K/N tails with scalar loads or masked vector paths.
- Ensure vectorized loads do not cross row boundaries.
- Use a padded shared tile (e.g. `[T][T+1]`) when access is column-wise.
- Check generated SASS/PTX and actual memory transactions; source-level `float4` does not guarantee a speedup.

### Performance
Vectorization reduces instruction overhead and may improve memory transaction formation; tiling provides the larger gain by reusing operands. Tensor Core implementations are often faster for supported data types/shapes.
