import type { CanvasSpec } from '$data/curriculum/types';

// GuidePane's Solution tab renders whatever this returns inside a code
// fence -- a canvas question has no code, so this renders the required
// connections as plain readable "A -> B" text instead.
export function renderCanvasSolution(spec: CanvasSpec): string {
	const labelByRef = new Map<string, string>();
	for (const node of spec.fixedNodes) labelByRef.set(node.id, node.label);
	for (const entry of spec.palette) labelByRef.set(`type:${entry.type}`, entry.label);

	return spec.requiredEdges
		.map(
			(edge) =>
				`${labelByRef.get(edge.from) ?? edge.from}  ->  ${labelByRef.get(edge.to) ?? edge.to}`
		)
		.join('\n');
}
