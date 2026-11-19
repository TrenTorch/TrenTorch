// Sparse formats and SpMV accounting (chapter E9).
export interface Csr {
	val: number[];
	col: number[];
	rowptr: number[];
}
export function toCsr(dense: number[][]): Csr {
	const val: number[] = [],
		col: number[] = [],
		rowptr = [0];
	for (const row of dense) {
		row.forEach((v, c) => {
			if (v !== 0) {
				val.push(v);
				col.push(c);
			}
		});
		rowptr.push(val.length);
	}
	return { val, col, rowptr };
}
export const toCoo = (dense: number[][]) =>
	dense.flatMap((row, r) => row.flatMap((v, c) => (v !== 0 ? [{ r, c, v }] : [])));
export const rowLengths = (csr: Csr) => csr.rowptr.slice(1).map((e, i) => e - csr.rowptr[i]);
/** ELL pads every row to the longest; waste = (rows*maxLen - nnz) / (rows*maxLen). */
export function ellStats(lengths: number[]) {
	const rows = lengths.length,
		maxLen = Math.max(...lengths),
		nnz = lengths.reduce((a, b) => a + b, 0);
	return {
		rows,
		maxLen,
		nnz,
		slots: rows * maxLen,
		waste: (rows * maxLen - nnz) / (rows * maxLen)
	};
}
/** Bytes per nonzero: COO 12, CSR ~8 + 4/row, ELL pads. */
export const bytesPerNnz = { coo: 12, csrValCol: 8, spmvGather: 12 } as const;
export const spmvAI = () => 2 / bytesPerNnz.spmvGather;
export const spmvBytes = (nnz: number) => nnz * bytesPerNnz.spmvGather;
/** Thread-per-row: a warp runs as long as its longest row; lane utilization = sum(len) / (32 * max(len)). */
export function threadPerRowUtilization(lengths: number[], lanes = 32) {
	let used = 0,
		slots = 0;
	for (let i = 0; i < lengths.length; i += lanes) {
		const w = lengths.slice(i, i + lanes);
		used += w.reduce((a, b) => a + b, 0);
		slots += lanes * Math.max(...w, 1);
	}
	return used / slots;
}
/** Warp-per-row: each row takes ceil(len/32) steps with `len` of 32 lanes active in total. */
export function warpPerRowUtilization(lengths: number[], lanes = 32) {
	const used = lengths.reduce((a, b) => a + b, 0),
		slots = lengths.reduce((a, l) => a + lanes * Math.max(1, Math.ceil(l / lanes)), 0);
	return used / slots;
}
/** Sectors touched by one warp load when lane i reads val[rowptr[r_i] + step] (thread-per-row). */
export function threadPerRowSectors(csr: Csr, firstRow: number, step: number, lanes = 32) {
	const addrs: number[] = [];
	for (let l = 0; l < lanes; l++) {
		const r = firstRow + l;
		if (r + 1 < csr.rowptr.length && csr.rowptr[r] + step < csr.rowptr[r + 1])
			addrs.push((csr.rowptr[r] + step) * 4);
	}
	return new Set(addrs.map((a) => Math.floor(a / 32))).size;
}
export const spmv = (csr: Csr, x: number[]) =>
	csr.rowptr.slice(1).map((end, r) => {
		let a = 0;
		for (let k = csr.rowptr[r]; k < end; k++) a += csr.val[k] * x[csr.col[k]];
		return a;
	});
