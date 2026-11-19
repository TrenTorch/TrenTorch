// The build-time validator for the CUDA theory chapters: structure, links in both directions, anchors, answers,
// figures and the guarantee that the authored text was copied, not rewritten.
import { describe, it, expect } from 'vitest';
import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { listCudaChapters, renderCudaChapter } from './read-course';
import { listCudaProblems } from './read-problems';
import { problemTheoryRefs } from './theory-links';
import { cudaToQuestionContent } from './to-question-content';
import { ALL_VIZ } from './viz';
import { workbook } from './model';

const READING_ORDER =
	'A1 A2 A3 A4 A5 B1 B2 B3 B4 B5 C1 C2 C3 D1 D2 D3 D4 D5 D6 E1 E2 E3 E4 E5 E6 E7 E8 E9 E10 F1 F2 F3 F4 F5 F7 F8 F9 F6 G1'.split(
		' '
	);
const chapters = listCudaChapters();
const problems = listCudaProblems();
const rendered = new Map(chapters.map((c) => [c.id, renderCudaChapter(c)]));
const md = (id: string) => readFileSync(chapters.find((c) => c.id === id)!.file, 'utf8');
const SRC = ['TRENTORCH_CUDA_THEORY.md', 'TRENTORCH_CUDA_THEORY_ADDENDUM.md'].map((f) =>
	readFileSync(join('docs', 'cuda', 'source', f), 'utf8')
);

describe('chapters', () => {
	it("has every chapter, in the addendum's reading order", () => {
		expect(chapters.map((c) => c.id)).toEqual(READING_ORDER);
		expect(new Set(chapters.map((c) => c.step)).size).toBe(chapters.length);
		for (const c of chapters) {
			expect(c.title.length).toBeGreaterThan(3);
			expect(c.estMinutes).toBeGreaterThan(0);
			expect('ABCDEFG').toContain(c.part);
		}
	});
	it('prerequisites name chapters that exist', () => {
		const ids = new Set(chapters.map((c) => c.id));
		for (const c of chapters)
			for (const p of c.prereqs) expect(ids.has(p), `${c.id} needs ${p}`).toBe(true);
	});
	it('every section anchor is unique within its chapter and slugifies cleanly', () => {
		for (const c of chapters) {
			const ids = rendered.get(c.id)!.toc.flatMap((t) => [t.id, ...t.sections.map((s) => s.id)]);
			expect(new Set(ids).size, `${c.id} has duplicate anchors`).toBe(ids.length);
			for (const id of ids) expect(id, c.id).toMatch(/^[a-z0-9][a-z0-9-]*$/);
		}
	});
	it('keeps every original section heading (they are the anchors problems link to)', () => {
		const src = SRC.join('\n'),
			keep: string[] = [];
		let fence = false;
		for (const l of src.split('\n')) {
			if (l.startsWith('```')) fence = !fence;
			if (!fence && l.startsWith('## ') && !l.includes('🎬')) keep.push(l.slice(3).trim());
		}
		const out = chapters.flatMap((c) =>
			md(c.id)
				.split('\n')
				.filter((l) => l.startsWith('## '))
				.map((l) => l.slice(3).trim())
		);
		const intentional = new Set([
			'How to use this file (for the agent)',
			'How the agent should merge this file',
			'A note on the PMPP references',
			'Reading order (updated)',
			'Original chapters: "Check yourself"',
			'G1 workbook answers',
			'Further reading',
			'Visual language (shared by every viz)',
			'Further reading (agent: add as a footer to each affected chapter)',
			'Small extensions to existing viz'
		]);
		const missing = [...new Set(keep)].filter(
			(h) => !out.includes(h) && !h.startsWith('Check yourself') && !intentional.has(h)
		);
		expect(missing).toEqual([]);
	});
	it('copies the authored code blocks exactly: partial code stays partial', () => {
		const all = chapters.map((c) => md(c.id)).join('\n');
		const blocks = SRC.flatMap((s) =>
			[...s.matchAll(/```[a-z]*\n([\s\S]*?)```/g)].map((m) => m[1])
		);
		// the box-drawing chip tree is drawn as a figure instead (chip-hierarchy), so its source block is not copied
		const outsideSpecs = blocks.filter((b) => !/🎬/.test(b) && !b.includes('├─'));
		expect(outsideSpecs.length).toBeGreaterThan(15);
		const missing = outsideSpecs.filter((b) => !all.includes(b));
		expect(missing.map((b) => b.slice(0, 60))).toEqual([]);
	});
	it('copies the authored prose: every source line survives, except structural lines the converter owns', () => {
		const out = new Set(
			chapters
				.flatMap((c) =>
					md(c.id)
						.split('\n')
						.map((l) => l.trim())
				)
				.filter(Boolean)
		);
		const gone: string[] = [];
		for (const [fi, src] of SRC.entries()) {
			let chapter = '',
				inSpec = false,
				fence = false,
				skip = false;
			for (const raw of src.split('\n')) {
				const l = raw.trim();
				if (raw.startsWith('```')) fence = !fence;
				if (/^# /.test(raw) && !fence) {
					chapter = raw;
					skip = !/^# (CHAPTER|NEW CHAPTER|APPEND TO)/.test(raw) || false;
					inSpec = false;
					continue;
				}
				if (skip || !chapter) continue;
				if (/^## /.test(raw) && !fence) inSpec = raw.includes('🎬');
				if (
					inSpec ||
					l === 'GPU' ||
					/^[├└│]/.test(l) ||
					!l ||
					l === '---' ||
					/^`id: /.test(l) ||
					/^## (Check yourself|Proposed problem)/.test(l) ||
					/^\d+\.\s/.test(l) ||
					/^\*\*Proposed:\*\*/.test(l) ||
					/^\*\*CU-\d+ .*\*\*:/.test(l) ||
					l.startsWith('**How the agent should use this chapter:**')
				)
					continue; // the G1 agent instruction is replaced by a learner-facing sentence
				if (!out.has(l)) gone.push(`${fi}: ${l.slice(0, 80)}`);
			}
		}
		expect(gone).toEqual([]);
	});
});

describe('problems and links', () => {
	const real = new Set(problems.map((p) => p.id));
	it('every [..](problem:CU-xxx) link resolves to a real problem and renders as a link into the IDE', () => {
		for (const c of chapters) {
			for (const m of md(c.id).matchAll(/\]\(problem:(CU-\d+)\)/g))
				expect(real.has(m[1]), `${c.id} links to missing ${m[1]}`).toBe(true);
			expect(rendered.get(c.id)!.html).not.toContain('problem:CU-');
		}
		expect(rendered.get('A2')!.html).toContain('href="/ide/cuda-vector-addition"');
	});
	it('chapters list real problems in their metadata and link to each of them in the body (and vice versa)', () => {
		for (const c of chapters) {
			for (const id of c.problems) {
				expect(real.has(id), `${c.id} lists ${id}`).toBe(true);
				expect(md(c.id), `${c.id} lists ${id} but never links it`).toContain(`problem:${id}`);
			}
		}
		const refs = problemTheoryRefs();
		for (const [id, list] of refs)
			for (const r of list)
				expect(
					chapters.find((c) => c.id === r.chapterId)!.problems.includes(id) ||
						md(r.chapterId).includes(`problem:${id}`)
				).toBe(true);
	});
	it('every problem the theory practises opens a theory link whose anchor exists', () => {
		let withTheory = 0;
		for (const p of problems) {
			const t = cudaToQuestionContent(p).metadata.theory;
			if (!t) continue;
			withTheory++;
			const c = chapters.find((x) => x.step === t.step)!;
			const ids = rendered.get(c.id)!.toc.flatMap((x) => [x.id, ...x.sections.map((s) => s.id)]);
			expect(ids, `${p.id} -> ${c.id}#${t.anchor}`).toContain(t.anchor);
		}
		expect(withTheory).toBeGreaterThanOrEqual(40);
	});
	it('proposed problems are "Coming soon" cards with no link and no failure', () => {
		const all = chapters.map((c) => md(c.id)).join('\n');
		for (const id of ['CU-053', 'CU-054', 'CU-056', 'CU-057']) {
			expect(all).toMatch(new RegExp(`coming-soon">.*${id}`));
			expect(real.has(id), `${id} is only a proposal`).toBe(false);
			expect(all).not.toContain(`problem:${id}`);
		}
		expect((all.match(/class="cs-badge">Coming soon/g) ?? []).length).toBe(4);
		expect(chapters.find((c) => c.id === 'E9')!.proposedProblems).toEqual(['CU-053']);
	});
});

describe('answers, math, tables, workbook', () => {
	const key = SRC[1].split('# ANSWER KEY')[1];
	it("puts each chapter's answers behind a Show answers toggle, never inline", () => {
		const answered = [...key.matchAll(/^\*\*(\w+)\.\*\*/gm)].map((m) => m[1]);
		expect(answered.length).toBeGreaterThanOrEqual(38);
		for (const id of answered) {
			const html = rendered.get(id)!.html;
			expect(html, id).toContain('<details class="answers"');
			expect(html, id).toContain('Show answers');
		}
		// the first answer of A1 appears only inside the toggle
		const a1 = rendered.get('A1')!.html;
		expect(a1.indexOf('<details class="answers"')).toBeLessThan(a1.indexOf('W/S = 10'));
	});
	it('G1: 34 problem cards, each with its own answer toggle and a Check form slot, matching the model', () => {
		const html = rendered.get('G1')!.html;
		expect((html.match(/class="g1-card"/g) ?? []).length).toBe(34);
		expect((html.match(/Show worked answer/g) ?? []).length).toBe(34);
		expect((html.match(/class="g1-check"/g) ?? []).length).toBe(34);
		expect(workbook().length).toBe(34);
	});
	it('renders KaTeX math and real tables', () => {
		expect(rendered.get('A5')!.html).toContain('katex');
		for (const id of ['A1', 'D1', 'D5', 'E9', 'F8'])
			expect(rendered.get(id)!.html, id).toContain('<table');
	});
});

describe('figures', () => {
	const specs = readdirSync('data/cuda/viz-specs')
		.filter((f) => f.startsWith('VIZ-'))
		.map((f) => f.slice(4, -3).toLowerCase());
	const ids = new Set(ALL_VIZ.map((c) => c.id));
	it('every figure placeholder has a saved spec and a component that draws it', () => {
		let count = 0;
		for (const c of chapters)
			for (const m of rendered
				.get(c.id)!
				.html.matchAll(/data-viz="VIZ-([A-Z0-9-]+)"[^>]*data-spec="VIZ-([A-Z0-9-]+)"/g)) {
				count++;
				const id = m[1].toLowerCase(),
					spec = m[2].toLowerCase();
				expect(specs, `${c.id} ${spec}`).toContain(spec);
				expect(ids.has(id), `${c.id}: no figure for ${id}`).toBe(true);
				expect(existsSync(`platform/components/cuda/viz/${id}/View.svelte`), `${id} view`).toBe(
					true
				);
			}
		expect(count).toBeGreaterThanOrEqual(60);
	});
	it('every spec in the source has a placeholder somewhere', () => {
		const placed = new Set(
			chapters.flatMap((c) =>
				[...rendered.get(c.id)!.html.matchAll(/data-spec="VIZ-([A-Z0-9-]+)"/g)].map((m) =>
					m[1].toLowerCase()
				)
			)
		);
		expect(specs.filter((s) => !placed.has(s))).toEqual([]);
	});
});
