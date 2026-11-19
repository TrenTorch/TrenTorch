<!-- chapters: D2 -->
## 🎬 VIZ-ROOFLINE-LADDER (extension of VIZ-ROOFLINE)
- Add a **Roof selector** (FP32 / TF32 / FP16), a **Tile size** slider that moves the matmul dot along the roofline using `B_M·B_N/(2(B_M+B_N))`, and a "required tile for compute-bound" readout.
