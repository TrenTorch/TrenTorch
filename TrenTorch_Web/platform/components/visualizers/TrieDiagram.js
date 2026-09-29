/**
 * @param {CanvasRenderingContext2D} context
 * @param {{ width: number; height: number; levels: Array<Array<{ label: string; x: number }>>; hitDepth: number }} options
 */
export function drawTrieDiagram(context, { width, height, levels, hitDepth }) {
	/** @param {number} level */
	const levelY = (level) => 38 + level * ((height - 72) / Math.max(1, levels.length - 1));
	/** @param {number} x */
	const nodeX = (x) => Math.max(36, Math.min(width - 36, x));
	const nodes = levels.flatMap((items, level) => items.map((item) => ({ ...item, level })));

	for (let level = 0; level < levels.length - 1; level++) {
		const parents = levels[level];
		const children = levels[level + 1];
		parents.forEach((parent, parentIndex) => {
			const firstChild = Math.floor((parentIndex * children.length) / parents.length);
			const lastChild = Math.max(
				firstChild,
				Math.floor(((parentIndex + 1) * children.length) / parents.length) - 1
			);
			for (let index = firstChild; index <= lastChild; index++) {
				context.beginPath();
				context.moveTo(nodeX(parent.x), levelY(level) + 14);
				context.lineTo(nodeX(children[index].x), levelY(level + 1) - 14);
				context.strokeStyle = level < hitDepth ? '#34d399' : '#f87171';
				context.stroke();
			}
		});
	}

	nodes.forEach((node) => {
		const color = node.level <= hitDepth ? '#14532d' : '#7f1d1d';
		context.fillStyle = color;
		context.fillRect(nodeX(node.x) - 35, levelY(node.level) - 12, 70, 24);
		context.fillStyle = node.level <= hitDepth ? '#a7f3d0' : '#fecaca';
		context.fillText(node.label, nodeX(node.x) - 29, levelY(node.level));
	});
}
