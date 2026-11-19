<!-- chapters: E4 -->
## 🎬 VIZ-IM2COL: "Convolution as a big matrix" (chapter E4)
- *Canvas:* a small input image, filter window sliding, and the im2col matrix filling one row per window.
- *Controls:* **K (1, 3, 5)**, **Input size**, **C_in**, **Implicit GEMM** toggle.
- *Readouts:* **matrix size**, **memory blow-up (≈ K²×)**, **FLOPs**.
- *Aha moment:* implicit GEMM removes the blown-up buffer.
