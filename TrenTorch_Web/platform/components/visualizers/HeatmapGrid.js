/**
 * @param {CanvasRenderingContext2D} context
 * @param {{ x: number; y: number; width: number; height: number; values: number[][]; selectedRow?: number }} options
 */
export function drawHeatmapGrid(context, { x, y, width, height, values, selectedRow = -1 }) {
	const rowCount = Math.max(1, values.length);
	const columnCount = Math.max(1, ...values.map((row) => row.length));
	const cellWidth = width / columnCount;
	const cellHeight = height / rowCount;

	values.forEach((row, rowIndex) => {
		row.forEach((value, columnIndex) => {
			const shade = Math.round(35 + Math.min(1, Math.max(0, value)) * 190);
			context.fillStyle =
				rowIndex === selectedRow
					? `rgb(${shade},95,${230 - shade / 2})`
					: `rgba(96,165,250,${0.18 + Math.min(1, Math.max(0, value))})`;
			context.fillRect(
				x + columnIndex * cellWidth,
				y + rowIndex * cellHeight,
				cellWidth - 3,
				cellHeight - 3
			);
			context.strokeStyle = 'rgba(255,255,255,.12)';
			context.strokeRect(
				x + columnIndex * cellWidth,
				y + rowIndex * cellHeight,
				cellWidth - 3,
				cellHeight - 3
			);
		});
	});
}
