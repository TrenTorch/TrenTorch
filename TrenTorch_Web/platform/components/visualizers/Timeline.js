/**
 * @typedef {{ label: string; start: number; duration: number; lane: number; color: string; kind?: 'tick' | 'bar' }} TimelineEvent
 */

/**
 * @param {CanvasRenderingContext2D} context
 * @param {{ x: number; y: number; width: number; height: number; duration: number; lanes: string[]; events: TimelineEvent[] }} options
 */
export function drawTimeline(context, { x, y, width, height, duration, lanes, events }) {
	const laneHeight = height / Math.max(1, lanes.length);
	const timeWidth = Math.max(1, width - 54);
	context.strokeStyle = '#3f3f46';
	context.beginPath();
	context.moveTo(x + 50, y);
	context.lineTo(x + width, y);
	context.stroke();

	lanes.forEach((name, index) => {
		const laneY = y + index * laneHeight;
		context.fillStyle = '#a1a1aa';
		context.fillText(name, x, laneY + laneHeight / 2);
		context.strokeStyle = 'rgba(255,255,255,.08)';
		context.beginPath();
		context.moveTo(x + 50, laneY + laneHeight);
		context.lineTo(x + width, laneY + laneHeight);
		context.stroke();
	});

	events.forEach((event) => {
		const eventX = x + 50 + (event.start / duration) * timeWidth;
		const eventY = y + event.lane * laneHeight + laneHeight * 0.2;
		const eventWidth = Math.max(3, (event.duration / duration) * timeWidth);
		context.fillStyle = event.color;
		if (event.kind === 'tick') {
			context.fillRect(eventX, eventY, 3, laneHeight * 0.6);
		} else {
			context.fillRect(eventX, eventY, eventWidth, laneHeight * 0.6);
			context.fillStyle = '#09090b';
			context.fillText(event.label, eventX + 3, eventY + laneHeight * 0.3);
		}
	});
}
