/**
 * @param {CanvasRenderingContext2D} context
 * @param {{ x: number; y: number; width: number; blocks: Array<string | null>; columns?: number }} options
 */
export function drawMemoryBlockGrid(context, { x, y, width, blocks, columns = 10 }) {
	const rows = Math.ceil(blocks.length / columns);
	const cellWidth = width / columns;
	const cellHeight = Math.max(20, Math.min(30, 120 / rows));
	const palette = ['#fb7185', '#60a5fa', '#34d399', '#fbbf24', '#c084fc', '#22d3ee'];

	blocks.forEach((owner, index) => {
		const column = index % columns;
		const row = Math.floor(index / columns);
		const cellX = x + column * cellWidth;
		const cellY = y + row * cellHeight;
		context.fillStyle = owner === null ? '#27272a' : palette[Number(owner) % palette.length];
		context.fillRect(cellX, cellY, cellWidth - 4, cellHeight - 4);
		context.strokeStyle = 'rgba(255,255,255,.14)';
		context.strokeRect(cellX, cellY, cellWidth - 4, cellHeight - 4);
		context.fillStyle = owner === null ? '#a1a1aa' : '#09090b';
		context.fillText(
			owner === null ? 'free' : `S${Number(owner) + 1}`,
			cellX + 3,
			cellY + cellHeight / 2
		);
	});
}
