// `<` is escaped so no string inside the data (a question title, say) can
// close the script element early. JSON.stringify alone does not do that.
// The replacement is the six characters < (a JSON escape), not a `<`.
export function toJsonLdScript(data: object): string {
	const json = JSON.stringify(data).replace(/</g, '\\u003c');
	return `<script type="application/ld+json">${json}</script>`;
}
