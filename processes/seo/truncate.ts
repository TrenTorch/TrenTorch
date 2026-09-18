// Cuts at a word boundary and adds an ellipsis, so a meta description stays
// under the ~160 characters search engines show before truncating it.
export function truncate(text: string, max: number): string {
	if (text.length <= max) return text;
	const cut = text.slice(0, max - 1);
	const lastSpace = cut.lastIndexOf(' ');
	return `${(lastSpace > max * 0.6 ? cut.slice(0, lastSpace) : cut).trimEnd()}…`;
}
