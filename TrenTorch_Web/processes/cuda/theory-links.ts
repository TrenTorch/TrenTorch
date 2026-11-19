// The theory <-> problem links, in both directions. Chapters link to problems from their Practice sections;
// every problem page then shows "Read the theory" pointing at the section that practises it (build time, so
// the two sides cannot drift apart).
import { readFileSync } from 'node:fs';
import { headingSlug } from '../dsa-theory/read-theory';
import { listCudaChapters } from './read-course';

export interface TheoryRef {
	chapterId: string;
	chapter: string;
	anchor: string;
	heading: string;
}

/** problem id (CU-xxx) -> every chapter section that links to it, in reading order. */
let cache: Map<string, TheoryRef[]> | null = null;
export function problemTheoryRefs(): Map<string, TheoryRef[]> {
	if (cache) return cache;
	const out = new Map<string, TheoryRef[]>();
	for (const c of listCudaChapters()) {
		let heading = '',
			anchor = '',
			fence = false;
		for (const line of readFileSync(c.file, 'utf8').split('\n')) {
			if (/^```/.test(line)) fence = !fence;
			if (fence) continue;
			const h = /^## (.+)$/.exec(line);
			if (h) {
				heading = h[1];
				anchor = headingSlug(h[1]);
			}
			for (const m of line.matchAll(/\]\(problem:(CU-\d+)\)/g)) {
				const list = out.get(m[1]) ?? [];
				if (!list.some((r) => r.chapterId === c.id && r.anchor === anchor))
					list.push({ chapterId: c.id, chapter: c.step, anchor, heading });
				out.set(m[1], list);
			}
		}
	}
	cache = out;
	return out;
}
