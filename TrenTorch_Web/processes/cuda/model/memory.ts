// Global-memory coalescing and shared-memory banks (chapters D1, D3, D5, A4).
export const SECTOR = 32;
export const BANKS = 32;

export const gcd = (a: number, b: number): number => (b === 0 ? Math.abs(a) : gcd(b, a % b));

/** Distinct 32-byte sectors touched by accesses of `width` bytes at the given byte addresses. */
export function sectors(addresses: number[], width = 4, sector = SECTOR) {
	const set = new Set<number>();
	for (const a of addresses)
		for (let s = Math.floor(a / sector); s <= Math.floor((a + width - 1) / sector); s++) set.add(s);
	return set;
}
/** Useful bytes divided by bytes the memory system fetched. */
export function coalescingEfficiency(addresses: number[], width = 4) {
	const n = sectors(addresses, width).size;
	return (addresses.length * width) / (n * SECTOR);
}
/** Addresses of a warp that reads element `lane * stride` (in elements of `width` bytes). */
export const strideAddresses = (stride: number, width = 4, offsetBytes = 0, lanes = 32) =>
	Array.from({ length: lanes }, (_, l) => offsetBytes + l * stride * width);
export function strideReport(stride: number, width = 4, offsetBytes = 0) {
	const a = strideAddresses(stride, width, offsetBytes);
	const set = sectors(a, width);
	const spanBytes = a[a.length - 1] - a[0] + width;
	return {
		sectors: set.size,
		efficiency: (a.length * width) / (set.size * SECTOR),
		spanBytes,
		bytesFetched: set.size * SECTOR
	};
}
/** Useful bandwidth under a bad pattern: efficiency x eta x peak. */
export const usefulBandwidth = (efficiency: number, eta: number, peak: number) =>
	efficiency * eta * peak;

/** Naive N x N transpose: reads coalesced, writes one sector per element (12.5%). Returns actual / ideal bytes. */
export function naiveTransposeBytes(n: number, writeEfficiency = 0.125) {
	const ideal = 8 * n * n;
	const actual = 4 * n * n + (4 * n * n) / writeEfficiency;
	return { ideal, actual, ratio: actual / ideal };
}

/** float4 bookkeeping for N elements (D3). */
export function float4Plan(n: number, blockThreads: number) {
	const vec = Math.floor(n / 4),
		tail = n % 4;
	return {
		vec,
		tail,
		blocks: Math.ceil(vec / blockThreads),
		scalarWarpLoads: n / 32,
		vectorWarpLoads: n / 128
	};
}
export const bytesInFlightPerWarpLoad = (width: number) => 32 * width;

/** Bank conflict degree for a warp reading smem[stride * lane]: gcd(stride, 32). */
export const strideConflictDegree = (stride: number) => gcd(stride, BANKS);

/** General conflict degree: the most distinct 4-byte words that any one bank must serve (same word = broadcast). */
export function conflictDegree(wordIndices: number[]) {
	const perBank = new Map<number, Set<number>>();
	for (const w of wordIndices) {
		const b = ((w % BANKS) + BANKS) % BANKS;
		(perBank.get(b) ?? perBank.set(b, new Set()).get(b)!).add(w);
	}
	let worst = 0;
	for (const s of perBank.values()) worst = Math.max(worst, s.size);
	return worst;
}
/** Word index of tile[row][col] for a tile with `pitch` words per row, optionally XOR-swizzled. */
export const tileWord = (row: number, col: number, pitch: number, swizzle = false) =>
	row * pitch + (swizzle ? (col ^ (row % BANKS)) % BANKS : col);

/** Banks hit when 32 lanes read column `col` (lane = row) of a 32 x 32 tile. */
export function columnReadDegree(pitch: number, swizzle = false) {
	return conflictDegree(Array.from({ length: 32 }, (_, lane) => tileWord(lane, 0, pitch, swizzle)));
}
export function rowReadDegree(pitch: number, swizzle = false) {
	return conflictDegree(Array.from({ length: 32 }, (_, lane) => tileWord(0, lane, pitch, swizzle)));
}
/** Scan indexing fix: add index >> 5 (one pad word per 32). */
export const scanPad = (i: number) => i + (i >> 5);

/** Constant cache: one address per cycle, so d distinct addresses cost d cycles. */
export const constantReadCycles = (addresses: number[]) => new Set(addresses).size;
