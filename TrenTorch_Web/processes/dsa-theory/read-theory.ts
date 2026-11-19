// The DSA sheet's theory pages. Each step folder under data/app_data/14-dsa-sheet may hold a
// theory.md; it becomes the page /dsa/theory/<step>. A question links to one heading on that page
// through its `theory:` anchor (see processes/curriculum-build/build-question.mjs).
//
// Authoring format of a theory.md (plain Markdown plus two conventions):
//   - `# Chapter` and `## Section` headings. Every heading gets an anchor id, built by
//     `headingSlug` below, so "## 1.2 Selection sort" is reachable as #selection-sort.
//   - A ```python block directly followed by a ```cpp block is shown as one block with a
//     Python / C++ switch.
// Math is written $inline$ or $$display$$ (KaTeX), same as every other curriculum markdown.
import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { cppLanguage } from '@codemirror/lang-cpp';
import { pythonLanguage } from '@codemirror/lang-python';
import { classHighlighter, highlightCode } from '@lezer/highlight';
import DOMPurify from 'isomorphic-dompurify';
import { Marked } from 'marked';
import { markdownMath } from '../markdown/markdown-math';

export const SHEET_DIR = join('data', 'app_data', '14-dsa-sheet');

export interface TheoryStep {
	step: string;
	title: string;
	file: string;
	/** The rest of the step's meta.json (the CUDA course keeps id, part, pmpp, estMinutes there). */
	meta?: Record<string, unknown>;
}

export interface TocEntry {
	id: string;
	title: string;
	sections: { id: string; title: string }[];
}

export interface TheoryPage {
	step: string;
	title: string;
	html: string;
	toc: TocEntry[];
}

const stripPrefix = (name: string) => name.replace(/^\d+-/, '');

/** "1.2 Selection sort" -> "selection-sort"; "Chapter 3. Designing it" -> "designing-it". */
export function headingSlug(title: string): string {
	return title
		.replace(/^chapter\s+\d+\.?\s*/i, '')
		.replace(/^\d+(\.\d+)*\.?\s+/, '')
		.toLowerCase()
		.replace(/[`*_$\\]/g, '')
		.replace(/[^a-z0-9]+/g, '-')
		.replace(/^-+|-+$/g, '');
}

/** The steps under `dir` that have a theory.md, in folder order. */
export function listTheoryStepsIn(dir: string): TheoryStep[] {
	if (!existsSync(dir)) return [];
	return readdirSync(dir)
		.filter((name) => !name.startsWith('_') && !name.startsWith('.'))
		.filter((name) => statSync(join(dir, name)).isDirectory())
		.sort()
		.flatMap((name) => {
			const file = join(dir, name, 'theory.md');
			if (!existsSync(file)) return [];
			const meta = JSON.parse(readFileSync(join(dir, name, 'meta.json'), 'utf8')) as {
				title: string;
			};
			return [{ step: stripPrefix(name), title: meta.title, file, meta }];
		});
}

/** The DSA sheet's steps. */
export function listTheorySteps(): TheoryStep[] {
	return listTheoryStepsIn(SHEET_DIR);
}

// A python block followed by a cpp block (blank lines between are fine) becomes one tabbed block.
// The wrapper is a block-level <div>, and the blank lines around the fences let marked render the
// code inside it; the browser adds the Python / C++ switch (see CodeTabs in the page).
const PAIR = /```python\n([\s\S]*?)\n```[ \t]*\n+```cpp\n([\s\S]*?)\n```/g;

function groupCodeBlocks(markdown: string): string {
	return markdown.replace(
		PAIR,
		(_all, py: string, cpp: string) =>
			`<div class="code-tabs">\n\n\`\`\`python\n${py}\n\`\`\`\n\n\`\`\`cpp\n${cpp}\n\`\`\`\n\n</div>`
	);
}

// Quotes are escaped too, so the result is safe inside an attribute as well as between tags.
const escapeHtml = (text: string) =>
	text
		.replace(/&/g, '&amp;')
		.replace(/</g, '&lt;')
		.replace(/>/g, '&gt;')
		.replace(/"/g, '&quot;')
		.replace(/'/g, '&#39;');

/** Colours a code block at build time with the same parsers the code editor uses. */
function highlight(code: string, lang: string | undefined): string {
	const language =
		lang === 'python' ? pythonLanguage : lang === 'cpp' || lang === 'cuda' ? cppLanguage : null;
	if (!language) return escapeHtml(code);
	const tree = language.parser.parse(code);
	let html = '';
	highlightCode(
		code,
		tree,
		classHighlighter,
		(text, classes) => {
			html += classes ? `<span class="${classes}">${escapeHtml(text)}</span>` : escapeHtml(text);
		},
		() => {
			html += '\n';
		}
	);
	return html;
}

/** Title -> question id for every question under a step folder, read from the README frontmatter. */
function questionIds(stepDir: string): Map<string, string> {
	const ids = new Map<string, string>();
	for (const topic of readdirSync(stepDir, { withFileTypes: true })) {
		if (!topic.isDirectory()) continue;
		for (const question of readdirSync(join(stepDir, topic.name), { withFileTypes: true })) {
			if (!question.isDirectory()) continue;
			const readme = join(stepDir, topic.name, question.name, 'README.md');
			if (!existsSync(readme)) continue;
			const head = readFileSync(readme, 'utf8').split('\n---')[0];
			const name = /^name: (.+)$/m.exec(head)?.[1]?.trim();
			const title = /^title: '?(.+?)'?\s*$/m.exec(head)?.[1];
			if (name && title) ids.set(title.replace(/''/g, "'"), name);
		}
	}
	return ids;
}

/** Turns "the problem *Name*" into a link to that question when the sheet has it. */
function linkQuestions(markdown: string, ids: Map<string, string>): string {
	return markdown.replace(
		/(problems?) (\*\*|\*|_)([^*_\n]+)\2/g,
		(all, word: string, _mark: string, title: string) => {
			const id = ids.get(title.trim());
			return id ? `${word} [${title}](/ide/${id})` : all;
		}
	);
}

export interface RenderOptions {
	/** Rewrites the markdown before rendering (the CUDA course resolves its problem links here). */
	transform?: (markdown: string) => string;
}

export function renderTheory(step: TheoryStep, options: RenderOptions = {}): TheoryPage {
	const raw = readFileSync(step.file, 'utf8');
	const markdown = options.transform ? options.transform(raw) : raw;
	const toc: TocEntry[] = [];
	const used = new Map<string, number>();
	const unique = (slug: string) => {
		const n = (used.get(slug) ?? 0) + 1;
		used.set(slug, n);
		return n === 1 ? slug : `${slug}-${n}`;
	};

	const marked = new Marked();
	marked.use(markdownMath({ throwOnError: false }));
	marked.use({
		renderer: {
			code({ text, lang }) {
				const language = lang?.trim().split(/\s+/)[0];
				// A class name is a plain word: anything else in a fence's language is dropped, not escaped.
				const safe = language && /^[A-Za-z0-9_+#.-]+$/.test(language) ? language : undefined;
				const cls = safe ? ` class="language-${escapeHtml(safe)}"` : '';
				return `<pre><code${cls}>${highlight(text, language)}</code></pre>\n`;
			},
			heading({ tokens, depth }) {
				const html = this.parser.parseInline(tokens);
				const text = tokens.map((t) => ('text' in t ? String(t.text) : '')).join('');
				const id = unique(headingSlug(text));
				if (depth === 1)
					toc.push({ id, title: text.replace(/^chapter\s+\d+\.\s*/i, ''), sections: [] });
				else if (depth === 2 && toc.length > 0) {
					toc[toc.length - 1].sections.push({ id, title: text.replace(/^\d+(\.\d+)*\.?\s+/, '') });
				}
				return `<h${depth} id="${id}">${html}</h${depth}>\n`;
			}
		}
	});

	const dirty = marked.parse(
		groupCodeBlocks(linkQuestions(markdown, questionIds(dirname(step.file)))),
		{ async: false }
	) as string;
	const html = DOMPurify.sanitize(dirty);
	return { step: step.step, title: step.title, html, toc };
}
