// Level-synchronous BFS (chapter E10).
export type Graph = number[][]; // adjacency lists
export interface BfsLevel {
	level: number;
	frontier: number[];
	edgesExamined: number;
	claims: number;
}
/** Push BFS: every frontier vertex examines all its neighbours and claims the unvisited ones. */
export function bfsPush(g: Graph, src: number): BfsLevel[] {
	const dist = Array(g.length).fill(-1);
	dist[src] = 0;
	let frontier = [src];
	const levels: BfsLevel[] = [];
	for (let level = 0; frontier.length; level++) {
		let edges = 0,
			claims = 0;
		const next: number[] = [];
		for (const u of frontier)
			for (const v of g[u]) {
				edges++;
				if (dist[v] < 0) {
					dist[v] = level + 1;
					next.push(v);
					claims++;
				}
			}
		levels.push({ level, frontier, edgesExamined: edges, claims });
		frontier = next;
	}
	return levels;
}
/** Pull BFS: every unvisited vertex scans its neighbours until it finds one in the frontier. */
export function bfsPull(g: Graph, src: number): BfsLevel[] {
	const dist = Array(g.length).fill(-1);
	dist[src] = 0;
	let frontier = [src];
	const levels: BfsLevel[] = [];
	for (let level = 0; frontier.length; level++) {
		const inF = new Set(frontier);
		let edges = 0;
		const next: number[] = [];
		for (let v = 0; v < g.length; v++) {
			if (dist[v] >= 0) continue;
			for (const u of g[v]) {
				edges++;
				if (inF.has(u)) {
					dist[v] = level + 1;
					next.push(v);
					break;
				}
			}
		}
		levels.push({ level, frontier, edgesExamined: edges, claims: next.length });
		frontier = next;
	}
	return levels;
}
export const bytesPerEdge = 4 + 32; // neighbour id + one 32-byte sector for dist[v]
export const bfsSweepSeconds = (edges: number, bw: number) => (edges * bytesPerEdge) / bw;
export const symmetric = (edges: [number, number][], n: number): Graph => {
	const g: Graph = Array.from({ length: n }, () => []);
	edges.forEach(([a, b]) => {
		g[a].push(b);
		g[b].push(a);
	});
	return g;
};
