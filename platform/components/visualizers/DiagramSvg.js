/** @param {{ label?: string }} [options] */
export function createDiagramSvg({ label = 'Interactive mathematical diagram' } = {}) {
	const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
	svg.setAttribute('viewBox', '0 0 600 280');
	svg.setAttribute('role', 'img');
	svg.setAttribute('aria-label', label);
	svg.classList.add('viz-diagram');
	return svg;
}

/** @param {string} name @param {Record<string, string | number>} [attributes] */
export function svgElement(name, attributes = {}) {
	const element = document.createElementNS('http://www.w3.org/2000/svg', name);
	for (const [key, value] of Object.entries(attributes)) {
		element.setAttribute(key, String(value));
	}
	return element;
}
