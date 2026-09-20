<script lang="ts">
	import {
		SvelteFlow,
		Background,
		Controls,
		type Node,
		type Edge,
		type Connection
	} from '@xyflow/svelte';
	import '@xyflow/svelte/dist/style.css';
	import CanvasNode from './CanvasNode.svelte';
	import type { CanvasSpec } from '$data/curriculum/types';
	import { GripVertical } from '@lucide/svelte';

	let {
		canvasSpec,
		nodes = $bindable([]),
		edges = $bindable([])
	} = $props<{
		canvasSpec: CanvasSpec;
		nodes?: Node[];
		edges?: Edge[];
	}>();

	const nodeTypes = { canvasNode: CanvasNode };

	// Fixed anchor nodes are (re-)seeded whenever `nodes` is empty --
	// +page.svelte resets `nodes`/`edges` to [] whenever the question
	// changes (including canvas-question to canvas-question navigation,
	// where this component instance is reused, not remounted), and this
	// effect re-runs on that reset, seeding from whatever `canvasSpec` is
	// current at that point. It never fights with what the student has
	// since dragged onto the canvas, since it only acts on a genuinely
	// empty graph.
	$effect(() => {
		if (nodes.length === 0) {
			nodes = canvasSpec.fixedNodes.map((n: CanvasSpec['fixedNodes'][number]) => ({
				id: n.id,
				type: 'canvasNode',
				position: n.position,
				data: { label: n.label, subtitle: n.subtitle, icon: n.icon },
				deletable: false
			}));
		}
	});

	let paletteGroups = $derived.by(() => {
		// Scratch value rebuilt on every run and never stored as state, so a
		// plain Map is correct here and a reactive SvelteMap would only add overhead.
		// eslint-disable-next-line svelte/prefer-svelte-reactivity
		const groups = new Map<string, CanvasSpec['palette']>();
		for (const entry of canvasSpec.palette) {
			const list = groups.get(entry.groupLabel) ?? [];
			list.push(entry);
			groups.set(entry.groupLabel, list);
		}
		return [...groups.entries()];
	});

	let dropCounter = 0;

	function handlePaletteDragStart(e: DragEvent, entryType: string) {
		e.dataTransfer?.setData('text/plain', entryType);
	}

	function handleCanvasDrop(e: DragEvent) {
		e.preventDefault();
		const type = e.dataTransfer?.getData('text/plain');
		const entry = canvasSpec.palette.find((p: CanvasSpec['palette'][number]) => p.type === type);
		if (!entry) return;
		dropCounter += 1;
		// Not the exact drop cursor position (that needs useSvelteFlow's
		// screenToFlowPosition, which requires a SvelteFlowProvider
		// ancestor) -- a staggered starting spot is enough, since every
		// node is freely draggable anywhere on the canvas immediately
		// after being created.
		const position = {
			x: 60 + ((dropCounter * 70) % 420),
			y: 260 + ((dropCounter * 90) % 320)
		};
		const id = `${entry.type}-${dropCounter}`;
		const newNode: Node = {
			id,
			type: 'canvasNode',
			position,
			data: {
				label: entry.label,
				subtitle: entry.subtitle,
				icon: entry.icon,
				paletteType: entry.type
			}
		};
		nodes = [...nodes, newNode];
	}

	function handleConnect(connection: Connection) {
		const id = `e-${connection.source}-${connection.target}-${edges.length}`;
		const newEdge: Edge = {
			id,
			source: connection.source,
			target: connection.target,
			animated: true,
			style: 'stroke: #f59e0b; stroke-width: 2; stroke-dasharray: 5 4;'
		};
		edges = [...edges, newEdge];
	}
</script>

<div class="flex h-full">
	<!-- Palette sidebar -->
	<div class="w-52 shrink-0 overflow-y-auto border-r border-border bg-secondary/30 p-3">
		<p class="mb-2 text-[10px] tracking-wider text-muted-foreground uppercase">
			Drag components from here
		</p>
		{#each paletteGroups as [groupLabel, entries] (groupLabel)}
			<p class="mt-3 mb-1.5 text-[10px] font-bold tracking-wider text-amber-500 uppercase">
				{groupLabel}
			</p>
			{#each entries as entry (entry.type)}
				<div
					draggable="true"
					ondragstart={(e) => handlePaletteDragStart(e, entry.type)}
					role="listitem"
					class="mb-1.5 flex cursor-grab items-center gap-2 rounded border border-border bg-background px-2 py-1.5 select-none active:cursor-grabbing"
				>
					<GripVertical class="size-3 shrink-0 text-muted-foreground" />
					<div class="min-w-0">
						<div class="truncate text-xs font-medium text-foreground">{entry.label}</div>
						{#if entry.subtitle}
							<div class="truncate text-[10px] text-muted-foreground">{entry.subtitle}</div>
						{/if}
					</div>
				</div>
			{/each}
		{/each}
	</div>

	<!-- Flow canvas: drag nodes freely, wire them by dragging from one
	     node's handle to another's -- both are @xyflow/svelte's own
	     built-in pointer interactions, not HTML5 drag-and-drop. -->
	<div
		class="relative flex-1 bg-black"
		ondragover={(e) => e.preventDefault()}
		ondrop={handleCanvasDrop}
		role="region"
		aria-label="Canvas"
	>
		<SvelteFlow
			bind:nodes
			bind:edges
			{nodeTypes}
			fitView
			fitViewOptions={{ padding: 0.2 }}
			minZoom={0.15}
			colorMode="dark"
			onconnect={handleConnect}
		>
			<Background />
			<Controls />
		</SvelteFlow>
	</div>
</div>
