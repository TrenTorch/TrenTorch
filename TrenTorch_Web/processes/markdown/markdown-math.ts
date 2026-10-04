// LaTeX math for the curriculum markdown ($inline$ and $$display$$), rendered with KaTeX.
//
// This replaces `marked-katex-extension`'s default rules, which only recognise a
// closing `$` that is followed by whitespace or one of `. , : ; ? !`. Real prose
// writes `($x$)`, `$k$-fold`, `$x$'s`, `$\mu$/$\sigma$`, and with the default rules
// all of those silently stayed as literal dollar signs, or paired a later `$` with
// the wrong one and showed a red KaTeX error. The library's own `nonStandard`
// switch fixes that but also turns prices ("$50,000 ... $60,000") into math.
//
// So this uses pandoc's rule instead: a closing `$` must not be followed by a
// digit. "$5 and $10" stays text; "$x$)" and "$k$-fold" render. Also accepted:
//   - `$$...$$` right after a line of text (not only after a space),
//   - a display block whose closing `$$` sits at the end of the formula line.
import katex from 'katex';
import type { MarkedExtension, TokenizerAndRendererExtension } from 'marked';

const INLINE = /^(\${1,2})(?!\$)((?:\\.|[^\\\n])*?(?:\\.|[^\\\n$]))\1(?!\d)/;
// `$$` or `$` alone on a line, formula on the following lines, same marker to close.
const BLOCK_FENCED = /^(\${1,2})\n((?:\\[^]|[^\\])+?)\n\1(?:\n|$)/;
// `$$ formula $$` as its own paragraph, on one line or several.
const BLOCK_DOUBLE = /^\$\$[ \t]*\n?((?:\\[^]|[^\\$])+?)\n?[ \t]*\$\$[ \t]*(?:\n|$)/;

export interface MarkdownMathOptions {
	throwOnError?: boolean;
}

type MathToken = { type: string; raw: string; text: string; displayMode: boolean };

export function markdownMath(options: MarkdownMathOptions = {}): MarkedExtension {
	const render = (token: MathToken, newline: boolean) =>
		katex.renderToString(token.text, {
			throwOnError: options.throwOnError ?? false,
			displayMode: token.displayMode
		}) + (newline ? '\n' : '');

	const inline: TokenizerAndRendererExtension = {
		name: 'inlineKatex',
		level: 'inline',
		start(src: string) {
			let from = 0;
			while (from < src.length) {
				const index = src.indexOf('$', from);
				if (index === -1) return undefined;
				// `\$` is an escaped dollar, not the start of math.
				if (src[index - 1] !== '\\' && INLINE.test(src.slice(index))) return index;
				from = index + 1;
				while (src[from] === '$') from++;
			}
			return undefined;
		},
		tokenizer(src: string) {
			const match = INLINE.exec(src);
			if (!match) return undefined;
			return {
				type: 'inlineKatex',
				raw: match[0],
				text: match[2].trim(),
				displayMode: match[1].length === 2
			};
		},
		renderer: (token) => render(token as MathToken, false)
	};

	const fenced: TokenizerAndRendererExtension = {
		name: 'blockKatex',
		level: 'block',
		tokenizer(src: string) {
			const match = BLOCK_FENCED.exec(src);
			if (!match) return undefined;
			return {
				type: 'blockKatex',
				raw: match[0],
				text: match[2].trim(),
				displayMode: match[1].length === 2
			};
		},
		renderer: (token) => render(token as MathToken, true)
	};

	const double: TokenizerAndRendererExtension = {
		name: 'blockKatexDouble',
		level: 'block',
		tokenizer(src: string) {
			const match = BLOCK_DOUBLE.exec(src);
			if (!match) return undefined;
			return { type: 'blockKatexDouble', raw: match[0], text: match[1].trim(), displayMode: true };
		},
		renderer: (token) => render(token as MathToken, true)
	};

	return { extensions: [inline, fenced, double] };
}
