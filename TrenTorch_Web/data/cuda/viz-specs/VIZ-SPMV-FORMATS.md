<!-- chapters: E9 -->
## 🎬 VIZ-SPMV-FORMATS: "Same matrix, four layouts"
- *Canvas:* a 16 × 16 sparse matrix (editable sparsity pattern or presets: banded, random, one dense row, power-law). Beside it, memory strips for COO, CSR, ELL.
- *Controls:* **Format**, **Mapping** (thread-per-row / warp-per-row), **Row-length distribution**, `Stepper`.
- *Animation:* for thread-per-row a `LaneStrip` shows lanes dropping out as short rows finish (divergence) while the longest row keeps the warp busy; for warp-per-row all lanes stay active on long rows but idle on short rows. Memory strip shows the addresses touched at each step, sectors lit as in VIZ-COALESCING.
- *Readouts:* **lane utilization %**, **sectors per load**, **padding waste %**, **bytes/nnz**.
- *Aha moment:* with one huge row, ELL wastes memory, scalar-CSR stalls a warp, and only nonzero-splitting stays balanced.
