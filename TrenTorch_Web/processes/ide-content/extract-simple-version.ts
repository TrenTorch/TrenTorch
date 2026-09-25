// Nearly every question's Theory opens with a plain-language "The simple
// version" section before the formal material. That section is the part
// worth putting in the static page: it explains the idea in a few
// sentences, which is what a search engine or an AI answer would quote.
// The rest of the Theory (formulas, code) stays behind its tab.
const HEADING = /^###\s+The simple version\s*$/im;

export function extractSimpleVersion(theoryMarkdown: string): string | null {
	const text = theoryMarkdown.replace(/\r\n/g, '\n');
	const match = HEADING.exec(text);
	if (!match) return null;

	const rest = text.slice(match.index + match[0].length);
	const nextHeading = rest.search(/^#{1,3}\s/m);
	const section = (nextHeading === -1 ? rest : rest.slice(0, nextHeading)).trim();
	return section || null;
}
