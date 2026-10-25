<script lang="ts">
	// A draggable divider between two panes, LeetCode-IDE style. Reports
	// pointer movement as a delta in pixels along its drag axis -- the
	// parent decides what that delta means (a width percent, a height
	// percent, clamped to whatever range makes sense for that split).
	let {
		axis,
		onResize,
		step = 24,
		valueNow,
		valueMin,
		valueMax,
		class: className = ''
	} = $props<{
		axis: 'x' | 'y'; // 'x' = drag left/right (a vertical divider bar); 'y' = drag up/down (a horizontal divider bar)
		onResize: (deltaPx: number) => void;
		step?: number; // px per arrow-key press, for keyboard resizing
		valueNow: number; // current size of the pane this edge controls, as a percent
		valueMin: number;
		valueMax: number;
		class?: string;
	}>();

	let dragging = $state(false);

	function handlePointerDown(e: PointerEvent) {
		const target = e.currentTarget as HTMLElement;
		target.setPointerCapture(e.pointerId);
		dragging = true;
		let lastPos = axis === 'x' ? e.clientX : e.clientY;

		function handlePointerMove(ev: PointerEvent) {
			const pos = axis === 'x' ? ev.clientX : ev.clientY;
			const delta = pos - lastPos;
			lastPos = pos;
			if (delta !== 0) onResize(delta);
		}

		function handlePointerUp() {
			dragging = false;
			target.removeEventListener('pointermove', handlePointerMove);
			target.removeEventListener('pointerup', handlePointerUp);
			target.removeEventListener('pointercancel', handlePointerUp);
		}

		target.addEventListener('pointermove', handlePointerMove);
		target.addEventListener('pointerup', handlePointerUp);
		target.addEventListener('pointercancel', handlePointerUp);
	}

	function handleKeydown(e: KeyboardEvent) {
		const negativeKey = axis === 'x' ? 'ArrowLeft' : 'ArrowUp';
		const positiveKey = axis === 'x' ? 'ArrowRight' : 'ArrowDown';
		if (e.key === negativeKey) {
			e.preventDefault();
			onResize(-step);
		} else if (e.key === positiveKey) {
			e.preventDefault();
			onResize(step);
		}
	}
</script>

<!-- A resizable window splitter is exactly the ARIA APG's role="separator"
     + tabindex + aria-value* pattern -- svelte-check's a11y linter doesn't
     recognize this as interactive, but it is (drag + arrow-key resize). -->
<!-- svelte-ignore a11y_no_noninteractive_tabindex -->
<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
<div
	role="separator"
	aria-orientation={axis === 'x' ? 'vertical' : 'horizontal'}
	aria-valuenow={Math.round(valueNow)}
	aria-valuemin={valueMin}
	aria-valuemax={valueMax}
	aria-label="Resize panes"
	tabindex="0"
	class="group relative shrink-0 touch-none select-none focus-visible:outline-none {axis === 'x'
		? 'w-2 cursor-col-resize'
		: 'h-2 cursor-row-resize'} {className}"
	onpointerdown={handlePointerDown}
	onkeydown={handleKeydown}
>
	<span
		class="pointer-events-none absolute rounded-full transition-colors group-hover:bg-foreground/30 group-focus-visible:bg-foreground/40 {axis ===
		'x'
			? 'inset-y-[38%] left-1/2 w-0.5 -translate-x-1/2'
			: 'inset-x-[38%] top-1/2 h-0.5 -translate-y-1/2'} {dragging ? 'bg-foreground/40' : ''}"
	></span>
</div>
