<!-- chapters: D6 -->
## 🎬 VIZ-REGISTER-PRESSURE: "The register budget"
- *Canvas:* a stacked bar for one SM's 65,536 registers, split into per-thread slices; to the right, a column of warp tokens showing how many warps are resident, and a small box "spilled to local memory".
- *Controls:* **Registers per thread** slider (16 → 255), **Block size**, **Profile**.
- *Animation:* increasing registers per thread shrinks the number of warp tokens in discrete steps; past the compiler limit a red portion labelled *spill* appears, and a bar "extra memory traffic" grows.
- *Aha moment:* two kernels with the same arithmetic can differ in speed only because one spills.
