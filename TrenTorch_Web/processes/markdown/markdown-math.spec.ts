import { describe, expect, it } from 'vitest';
import { Marked, type Token } from 'marked';
import { questionsById } from '$processes/ide-content/curriculum-index';
import { markdownMath } from './markdown-math';

function renderer() {
	const marked = new Marked();
	marked.use(markdownMath({ throwOnError: false }));
	return marked;
}

const render = (markdown: string) => renderer().parse(markdown, { async: false }) as string;
const mathCount = (html: string) => (html.match(/class="katex(-display)?"/g) ?? []).length;

describe('markdownMath: inline math next to punctuation', () => {
	it.each([
		['a closing bracket', 'the loss ($H^2 = I$) is small'],
		['a hyphen', 'the $k$-fold split'],
		['an apostrophe', "the $i$'s own angle"],
		['a slash', 'close to $\\mu$/$\\sigma$ but not exact'],
		['a semicolon', 'the point $(1,1)$; the area under the curve'],
		['a quote', 'row $j$" becomes'],
		['a possessive', 'matrix $A$’s columns'],
		['a colon', 'where $x$: a vector']
	])('renders math followed by %s', (_name, markdown) => {
		const html = render(markdown);
		expect(html).toContain('class="katex"');
		expect(html).not.toContain('katex-error');
		expect(html).not.toContain('$');
	});

	it('still renders math followed by a space, comma or full stop', () => {
		expect(mathCount(render('so $a$ and $b$, then $c$.'))).toBe(3);
	});
});

describe('markdownMath: dollar signs that are not math', () => {
	it('keeps prices as text', () => {
		const html = render('Costs $50,000 for the car and $60,000 for the truck, or $5 and $10.');
		expect(html).not.toContain('katex');
		expect(html).toContain('$50,000');
	});

	it('keeps an escaped dollar sign as text', () => {
		const html = render('Pay \\$5 and \\$6 today.');
		expect(html).not.toContain('katex');
	});

	it('leaves dollar signs in code alone', () => {
		const html = render('Run `echo $HOME` or\n\n```sh\nprice=$5; echo $price\n```');
		expect(html).not.toContain('katex');
	});
});

describe('markdownMath: display math', () => {
	it('renders $$ on its own lines', () => {
		expect(render('$$\nE = mc^2\n$$')).toContain('katex-display');
	});

	it('renders $$ whose closing marker ends the formula line', () => {
		const html = render(
			'### Formula\n\n$$\nf(x) = \\begin{cases} 1 & x > 0 \\\\ 0 & \\text{otherwise}\\end{cases}$$\n\n### Next'
		);
		expect(html).toContain('katex-display');
		expect(html).not.toContain('katex-error');
		expect(html).toContain('<h3>Next</h3>');
	});

	it('renders $$ on a line straight after text', () => {
		const html = render('Loss combines terms:\n$$\\mathcal{L} = ||x - \\hat{x}||^2$$');
		expect(html).toContain('katex-display');
		expect(html).not.toContain('$$');
	});
});

// Every question's Statement, Theory and Explanation, rendered the way the IDE renders them.
describe('markdownMath: the whole curriculum', () => {
	const marked = renderer();
	const sources = [...questionsById.values()].flatMap((q) => [
		{ id: q.id, part: 'statement', markdown: q.statementMarkdown },
		{ id: q.id, part: 'theory', markdown: q.theoryMarkdown ?? '' },
		{ id: q.id, part: 'explanation', markdown: q.oracleExplanationMarkdown ?? '' }
	]);

	it('has no KaTeX parse errors', () => {
		const broken = sources
			.filter(({ markdown }) =>
				(marked.parse(markdown, { async: false }) as string).includes('katex-error')
			)
			.map(({ id, part }) => `${id} (${part})`);
		expect(broken).toEqual([]);
	});

	it('leaves no unrendered $math$ behind in the text', () => {
		const leftovers: string[] = [];
		const visit = (tokens: Token[] | undefined, id: string) => {
			for (const token of tokens ?? []) {
				if (
					['code', 'codespan', 'inlineKatex', 'blockKatex', 'blockKatexDouble', 'html'].includes(
						token.type
					)
				)
					continue;
				const t = token as Token & { tokens?: Token[]; items?: { tokens?: Token[] }[] };
				if (
					(t.type === 'text' || t.type === 'escape') &&
					!t.tokens &&
					/\$[^\s\d]/.test(t.raw) &&
					!/\$\d/.test(t.raw)
				) {
					leftovers.push(`${id}: ${t.raw.replace(/\n/g, ' ').slice(0, 80)}`);
				}
				visit(t.tokens, id);
				t.items?.forEach((item) => visit(item.tokens, id));
			}
		};
		for (const { id, markdown } of sources) visit(marked.lexer(markdown), id);
		expect(leftovers).toEqual([]);
	});
});
