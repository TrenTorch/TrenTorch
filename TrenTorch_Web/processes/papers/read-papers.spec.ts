import { describe, it, expect, afterEach } from 'vitest';
import { mkdtempSync, mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { PAPERS_DIR, readPaperTopics, readPapers } from './read-papers';

const paperMeta = (overrides: Record<string, unknown> = {}) => ({
	title: 'Dropout',
	paper: {
		title: 'Improving neural networks by preventing co-adaptation of feature detectors',
		authors: 'G. Hinton',
		year: 2012,
		kind: 'foundational',
		summary: 'Randomly drop units.',
		arxivId: '1207.0580',
		...overrides
	}
});

const readme = (name: string, title: string, difficulty = 'Beginner') =>
	`---\nname: ${name}\ntitle: '${title}'\ntags: [research-papers]\ndifficulty: ${difficulty}\n---\n\n## Statement\n`;

interface PaperSpec {
	folder: string;
	meta?: object;
	exercises?: { folder: string; readme: string }[];
}

let dirs: string[] = [];
afterEach(() => {
	for (const dir of dirs) rmSync(dir, { recursive: true, force: true });
	dirs = [];
});

// Builds a throw-away copy of the papers folder layout.
function build(topics: { folder: string; meta?: object; papers: PaperSpec[] }[]): string {
	const base = mkdtempSync(join(tmpdir(), 'papers-'));
	dirs.push(base);
	const root = join(base, PAPERS_DIR);
	mkdirSync(root, { recursive: true });
	for (const topic of topics) {
		const topicDir = join(root, topic.folder);
		mkdirSync(topicDir, { recursive: true });
		writeFileSync(
			join(topicDir, 'meta.json'),
			JSON.stringify(topic.meta ?? { title: 'Topic', description: 'A topic.' })
		);
		for (const paper of topic.papers) {
			const paperDir = join(topicDir, paper.folder);
			mkdirSync(paperDir, { recursive: true });
			writeFileSync(join(paperDir, 'meta.json'), JSON.stringify(paper.meta ?? paperMeta()));
			for (const ex of paper.exercises ?? [
				{
					folder: '01-forward',
					readme: readme('research-dropout-forward', 'Dropout: The Forward Pass')
				}
			]) {
				mkdirSync(join(paperDir, ex.folder), { recursive: true });
				writeFileSync(join(paperDir, ex.folder, 'README.md'), ex.readme);
			}
		}
	}
	return base;
}

describe('readPaperTopics', () => {
	it('reads topics, papers and exercises from the folders, in folder order', () => {
		const base = build([
			{
				folder: '01-second',
				meta: { title: 'Second', description: 'b' },
				papers: [
					{
						folder: '01-x',
						meta: paperMeta({ arxivId: '1111.1111' }),
						exercises: [{ folder: '01-a', readme: readme('ex-x', 'X: Thing') }]
					}
				]
			},
			{
				folder: '00-first',
				meta: { title: 'First', description: 'a' },
				papers: [
					{ folder: '02-dropout' },
					{
						folder: '01-adam',
						meta: paperMeta({ arxivId: '1412.6980' }),
						exercises: [
							{ folder: '02-b', readme: readme('ex-adam-b', 'Adam: Second', 'Advanced') },
							{ folder: '01-a', readme: readme('ex-adam-a', 'Adam: First') }
						]
					}
				]
			}
		]);
		const topics = readPaperTopics(base);
		expect(topics.map((t) => t.slug)).toEqual(['first', 'second']);
		expect(topics[0].papers.map((p) => p.slug)).toEqual(['adam', 'dropout']);
		expect(topics[0].papers[0].implementations).toEqual([
			{ slug: 'ex-adam-a', title: 'First', difficulty: 'Beginner' },
			{ slug: 'ex-adam-b', title: 'Second', difficulty: 'Advanced' }
		]);
	});

	it('lets a paper keep a slug that differs from its folder name', () => {
		const base = build([
			{
				folder: '00-t',
				papers: [{ folder: '01-folder-name', meta: paperMeta({ slug: 'url-name' }) }]
			}
		]);
		expect(readPapers(base).map((p) => p.slug)).toEqual(['url-name']);
	});

	it('skips an empty topic folder', () => {
		const base = build([{ folder: '00-empty', papers: [] }]);
		expect(readPaperTopics(base)).toEqual([]);
	});

	it.each([
		['a missing field', { summary: '' }, /"summary"/],
		['an unknown kind', { kind: 'famous' }, /"kind"/],
		['a non-numeric year', { year: '2012' }, /"year"/],
		['an arXiv id with a prefix', { arxivId: 'arXiv:1207.0580' }, /"arxivId"/],
		['a bad slug', { slug: 'Not A Slug' }, /slug/]
	])('rejects %s with a message that names the file', (_label, bad, message) => {
		const base = build([{ folder: '00-t', papers: [{ folder: '01-p', meta: paperMeta(bad) }] }]);
		expect(() => readPaperTopics(base)).toThrow(message);
		expect(() => readPaperTopics(base)).toThrow(/meta\.json/);
	});

	it('rejects a paper with no exercises', () => {
		const base = build([{ folder: '00-t', papers: [{ folder: '01-p', exercises: [] }] }]);
		expect(() => readPaperTopics(base)).toThrow(/no exercise folders/);
	});

	it('rejects an exercise with an unknown difficulty', () => {
		const base = build([
			{
				folder: '00-t',
				papers: [
					{ folder: '01-p', exercises: [{ folder: '01-a', readme: readme('ex', 'T', 'Hard') }] }
				]
			}
		]);
		expect(() => readPaperTopics(base)).toThrow(/difficulty/);
	});

	it('rejects duplicate paper slugs and duplicate exercise names', () => {
		const dupPaper = build([
			{
				folder: '00-t',
				papers: [{ folder: '01-same' }, { folder: '02-other', meta: paperMeta({ slug: 'same' }) }]
			}
		]);
		expect(() => readPaperTopics(dupPaper)).toThrow(/Paper slug "same"/);
		const dupExercise = build([
			{ folder: '00-t', papers: [{ folder: '01-a' }, { folder: '02-b' }] }
		]);
		expect(() => readPaperTopics(dupExercise)).toThrow(/Exercise name "research-dropout-forward"/);
	});

	it('tells the author when a meta.json is missing', () => {
		const base = build([{ folder: '00-t', papers: [{ folder: '01-p' }] }]);
		rmSync(join(base, PAPERS_DIR, '00-t', '01-p', 'meta.json'));
		expect(() => readPaperTopics(base)).toThrow(/Missing .*meta\.json/);
	});
});

describe('the real papers folder', () => {
	const topics = readPaperTopics();
	const papers = topics.flatMap((t) => t.papers);

	it('parses, with unique paper slugs and exercise names', () => {
		expect(topics.length).toBeGreaterThan(0);
		expect(new Set(papers.map((p) => p.slug)).size).toBe(papers.length);
		const exercises = papers.flatMap((p) => p.implementations.map((i) => i.slug));
		expect(new Set(exercises).size).toBe(exercises.length);
	});

	it('gives every paper at least one exercise', () => {
		for (const paper of papers) expect(paper.implementations.length).toBeGreaterThan(0);
	});
});
