## Small extensions to existing viz

- **VIZ-INDEX-CALCULATOR (B1):** add a **"32-bit index"** toggle that wraps the product at 2³¹ for N = 3×10⁹ and shows threads reading the wrong element.
- **VIZ-FLOAT4-BANDWIDTH (D3):** add a **tail panel** showing 250,000 float4 elements plus 3 scalar tail elements for N = 1,000,003.
- **VIZ-ATOMIC-CONTENTION (E5):** add a **warp-aggregated** mode where lanes with the same bin merge into one atomic via `ballot/popc`.
- **VIZ-MAP-FLOW (E1):** show **blocks = capacity C** (SMs × blocks/SM) when grid-stride mode is chosen.
- **VIZ-MEMORY-LADDER (A4):** add a **"copy-kernel benchmark"** button that shows achieved ≈ 80-90% of peak bandwidth.
