// Convolution accounting (chapter E4).
export const convFlops = (n: number, cin: number, cout: number, h: number, w: number, k: number) =>
	2 * n * cout * h * w * cin * k * k;
export const convBytes = (
	n: number,
	cin: number,
	cout: number,
	h: number,
	w: number,
	k: number
) => ({
	input: n * cin * h * w * 4,
	output: n * cout * h * w * 4,
	weights: cout * cin * k * k * 4
});
export const im2colBytes = (n: number, cin: number, h: number, w: number, k: number) =>
	n * h * w * cin * k * k * 4;
export const im2colBlowup = (k: number) => k * k;
/** Loads per output for a T x T tile with a (K-1)/2 halo. */
export const haloOverhead2D = (tx: number, ty: number, k: number) =>
	((tx + k - 1) * (ty + k - 1)) / (tx * ty);
export const haloOverhead3D = (t: number, k: number) => (t + k - 1) ** 3 / t ** 3;
/** Separable K x K filter: two 1-D passes. */
export const separableMacs = (k: number) => ({ direct: k * k, separable: 2 * k });
export const conv2dDirect = (img: number[][], f: number[][]) => {
	const h = img.length,
		w = img[0].length,
		fh = f.length,
		fw = f[0].length,
		out: number[][] = [];
	for (let y = 0; y < h; y++) {
		out.push([]);
		for (let x = 0; x < w; x++) {
			let a = 0;
			for (let ky = 0; ky < fh; ky++)
				for (let kx = 0; kx < fw; kx++) {
					const iy = y + ky - (fh >> 1),
						ix = x + kx - (fw >> 1);
					if (iy >= 0 && iy < h && ix >= 0 && ix < w) a += img[iy][ix] * f[ky][kx];
				}
			out[y].push(a);
		}
	}
	return out;
};
/** im2col: one row per output pixel, K*K*Cin columns (single channel when cin = 1). */
export function im2col(img: number[][], k: number) {
	const h = img.length,
		w = img[0].length,
		rows: number[][] = [];
	for (let y = 0; y < h; y++)
		for (let x = 0; x < w; x++) {
			const r: number[] = [];
			for (let ky = 0; ky < k; ky++)
				for (let kx = 0; kx < k; kx++) {
					const iy = y + ky - (k >> 1),
						ix = x + kx - (k >> 1);
					r.push(iy >= 0 && iy < h && ix >= 0 && ix < w ? img[iy][ix] : 0);
				}
			rows.push(r);
		}
	return rows;
}
