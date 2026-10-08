// The research-papers section is read straight from the folders under
// data/app_data/12-research-papers, so adding a paper (or sixty) means adding
// folders, never editing code. The layout, one level per folder:
//
//   12-research-papers/
//     <NN>-<topic>/               meta.json: { "title", "description" }
//       <NN>-<paper>/             meta.json: { "title", "paper": { ... } }
//         <NN>-<exercise>/        README.md frontmatter: name, title, difficulty
//
// The numeric prefixes only set the display order. Everything is validated here, at build
// time, with an error that names the file to fix. See the README in the papers folder.
import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import type { Paper, PaperImplementation, PaperKind, PaperTopic } from './types';

export const PAPERS_DIR = join('data', 'app_data', '12-research-papers');

const KINDS: PaperKind[] = ['foundational', 'breakthrough'];
const DIFFICULTIES: PaperImplementation['difficulty'][] = ['Beginner', 'Intermediate', 'Advanced'];
// New-style ids (1207.0580) and old-style ids (cs/0112017). A version suffix (v2) is not part of the id.
const ARXIV_ID = /^(\d{4}\.\d{4,5}|[a-z-]+(\.[A-Z]{2})?\/\d{7})$/;
const SLUG = /^[a-z0-9]+(-[a-z0-9]+)*$/;

const stripPrefix = (name: string) => name.replace(/^\d+-/, '');

function contentDirs(dir: string): string[] {
	return readdirSync(dir)
		.filter((name) => !name.startsWith('_') && !name.startsWith('.'))
		.filter((name) => statSync(join(dir, name)).isDirectory())
		.sort();
}

function readJson(path: string): Record<string, unknown> {
	if (!existsSync(path)) throw new Error(`Missing ${path}`);
	try {
		const value: unknown = JSON.parse(readFileSync(path, 'utf8'));
		if (typeof value !== 'object' || value === null || Array.isArray(value)) {
			throw new Error('expected a JSON object');
		}
		return value as Record<string, unknown>;
	} catch (err) {
		throw new Error(`Invalid ${path}: ${(err as Error).message}`, { cause: err });
	}
}

function text(value: unknown, field: string, path: string): string {
	if (typeof value !== 'string' || value.trim() === '') {
		throw new Error(`${path}: "${field}" must be a non-empty string`);
	}
	return value.trim();
}

function frontmatter(path: string): Record<string, string> {
	if (!existsSync(path)) throw new Error(`Missing ${path}`);
	const match = readFileSync(path, 'utf8').match(/^---\r?\n([\s\S]*?)\r?\n---/);
	if (!match) throw new Error(`${path} is missing its --- frontmatter block`);
	const fields: Record<string, string> = {};
	for (const line of match[1].split(/\r?\n/)) {
		const colon = line.indexOf(':');
		if (colon === -1) continue;
		const value = line.slice(colon + 1).trim();
		fields[line.slice(0, colon).trim()] = value.replace(/^(['"])(.*)\1$/, '$2');
	}
	return fields;
}

// "Dropout: The Forward Pass With Inverted Scaling" -> "The Forward Pass With Inverted Scaling":
// inside a paper's own list the paper name is redundant.
function exerciseTitle(title: string): string {
	const colon = title.indexOf(': ');
	return colon > 0 && colon < title.length - 2 ? title.slice(colon + 2) : title;
}

function readImplementations(paperDir: string): PaperImplementation[] {
	return contentDirs(paperDir).map((name) => {
		const file = join(paperDir, name, 'README.md');
		const fm = frontmatter(file);
		const difficulty = fm.difficulty as PaperImplementation['difficulty'];
		if (!DIFFICULTIES.includes(difficulty)) {
			throw new Error(`${file}: difficulty must be one of ${DIFFICULTIES.join(', ')}`);
		}
		return {
			slug: text(fm.name, 'name', file),
			title: exerciseTitle(text(fm.title, 'title', file)),
			difficulty
		};
	});
}

function readPaper(paperDir: string, folderName: string): Paper {
	const metaPath = join(paperDir, 'meta.json');
	const meta = readJson(metaPath);
	const raw = meta.paper;
	if (typeof raw !== 'object' || raw === null || Array.isArray(raw)) {
		throw new Error(
			`${metaPath} needs a "paper" object (title, authors, year, kind, summary, arxivId)`
		);
	}
	const paper = raw as Record<string, unknown>;
	const slug =
		paper.slug === undefined ? stripPrefix(folderName) : text(paper.slug, 'slug', metaPath);
	if (!SLUG.test(slug))
		throw new Error(`${metaPath}: slug "${slug}" must be lower-case words joined by "-"`);
	const kind = paper.kind as PaperKind;
	if (!KINDS.includes(kind))
		throw new Error(`${metaPath}: "kind" must be one of ${KINDS.join(', ')}`);
	const year = paper.year;
	if (typeof year !== 'number' || !Number.isInteger(year) || year < 1950 || year > 2100) {
		throw new Error(`${metaPath}: "year" must be a four-digit number`);
	}
	const arxivId = text(paper.arxivId, 'arxivId', metaPath);
	if (!ARXIV_ID.test(arxivId)) {
		throw new Error(
			`${metaPath}: "arxivId" must look like 1207.0580 (no "arXiv:" prefix, no version)`
		);
	}
	const implementations = readImplementations(paperDir);
	if (implementations.length === 0) {
		throw new Error(`${paperDir} has no exercise folders (each needs a README.md)`);
	}
	return {
		slug,
		title: text(paper.title, 'title', metaPath),
		authors: text(paper.authors, 'authors', metaPath),
		year,
		kind,
		summary: text(paper.summary, 'summary', metaPath),
		arxivId,
		implementations
	};
}

export function readPaperTopics(baseDir: string = process.cwd()): PaperTopic[] {
	const root = join(baseDir, PAPERS_DIR);
	const topics: PaperTopic[] = [];
	const paperSlugs = new Map<string, string>();
	const exerciseSlugs = new Map<string, string>();

	for (const topicName of contentDirs(root)) {
		const topicDir = join(root, topicName);
		const meta = readJson(join(topicDir, 'meta.json'));
		const papers: Paper[] = [];
		for (const paperName of contentDirs(topicDir)) {
			const paperDir = join(topicDir, paperName);
			const paper = readPaper(paperDir, paperName);
			const earlier = paperSlugs.get(paper.slug);
			if (earlier)
				throw new Error(`Paper slug "${paper.slug}" is used by both ${earlier} and ${paperDir}`);
			paperSlugs.set(paper.slug, paperDir);
			for (const impl of paper.implementations) {
				const clash = exerciseSlugs.get(impl.slug);
				if (clash)
					throw new Error(`Exercise name "${impl.slug}" is used in both ${clash} and ${paperDir}`);
				exerciseSlugs.set(impl.slug, paperDir);
			}
			papers.push(paper);
		}
		if (papers.length === 0) continue; // an empty topic folder is a placeholder
		topics.push({
			slug: stripPrefix(topicName),
			title: text(meta.title, 'title', join(topicDir, 'meta.json')),
			description: text(meta.description, 'description', join(topicDir, 'meta.json')),
			papers
		});
	}
	return topics;
}

export function readPapers(baseDir?: string): Paper[] {
	return readPaperTopics(baseDir).flatMap((topic) => topic.papers);
}
