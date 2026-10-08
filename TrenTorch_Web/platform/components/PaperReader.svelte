<script lang="ts">
	import { browser } from '$app/environment';
	import { tick, untrack } from 'svelte';
	import { SvelteMap } from 'svelte/reactivity';
	import type { PDFDocumentProxy } from 'pdfjs-dist';
	import {
		ZoomIn,
		ZoomOut,
		ExternalLink,
		Loader,
		Hand,
		Pencil,
		Highlighter,
		Type,
		Eraser,
		Undo2,
		Trash
	} from '@lucide/svelte';

	interface Props {
		url: string;
		title: string;
		fallbackHref: string;
	}

	let { url, title, fallbackHref }: Props = $props();

	const ZOOM_STEPS = [0.75, 1, 1.25, 1.5, 2];
	const PAGE_MAX_WIDTH = 820;

	let zoomIndex = $state(1);
	let pageCount = $state(0);
	let currentPage = $state(1);
	let pageRatio = $state(1.294);
	let status = $state<'loading' | 'ready' | 'error'>('loading');
	let scrollEl = $state<HTMLDivElement | null>(null);
	let readerEl = $state<HTMLElement | null>(null);
	// True after the last pointer press landed inside the viewer: arrow keys then scroll
	// the paper, otherwise they keep scrolling the page.
	let viewerActive = false;
	let pagesEl = $state<HTMLDivElement | null>(null);
	let pageWidth = $state(PAGE_MAX_WIDTH);

	let pdf: PDFDocumentProxy | null = null;
	const renderedAt = new SvelteMap<number, string>();
	let observers: IntersectionObserver[] = [];

	const scale = $derived(ZOOM_STEPS[zoomIndex]);
	const pageNumbers = $derived(Array.from({ length: pageCount }, (_, i) => i + 1));

	async function renderPage(canvas: HTMLCanvasElement, pageNumber: number) {
		if (!pdf) return;
		const zoom = untrack(() => scale);
		const width = untrack(() => pageWidth);
		const key = `${zoom}|${width}`;
		if (renderedAt.get(pageNumber) === key) return;
		renderedAt.set(pageNumber, key);
		const page = await pdf.getPage(pageNumber);
		const dpr = Math.min(window.devicePixelRatio || 1, 2);
		const cssWidth = width * zoom;
		const base = page.getViewport({ scale: 1 });
		const viewport = page.getViewport({ scale: (cssWidth / base.width) * dpr });
		canvas.width = Math.floor(viewport.width);
		canvas.height = Math.floor(viewport.height);
		canvas.style.width = `${cssWidth}px`;
		canvas.style.height = `${(cssWidth * base.height) / base.width}px`;
		const ctx = canvas.getContext('2d');
		if (!ctx) return;
		await page.render({ canvasContext: ctx, viewport, canvas }).promise;
	}

	function frames(): HTMLDivElement[] {
		return pagesEl ? [...pagesEl.querySelectorAll<HTMLDivElement>('[data-page]')] : [];
	}

	function observeFrames() {
		const root = scrollEl;
		const renderObserver = new IntersectionObserver(
			(entries) => {
				for (const entry of entries) {
					if (!entry.isIntersecting) continue;
					const frame = entry.target as HTMLDivElement;
					const canvas = frame.querySelector('canvas');
					if (canvas) void renderPage(canvas, Number(frame.dataset.page));
				}
			},
			{ root, rootMargin: '800px 0px' }
		);
		const pageObserver = new IntersectionObserver(
			(entries) => {
				for (const entry of entries) {
					if (entry.isIntersecting)
						currentPage = Number((entry.target as HTMLElement).dataset.page);
				}
			},
			{ root, threshold: 0.55 }
		);
		for (const frame of frames()) {
			renderObserver.observe(frame);
			pageObserver.observe(frame);
		}
		observers = [renderObserver, pageObserver];
	}

	$effect(() => {
		const source = url;
		if (!browser) return;
		let cancelled = false;

		(async () => {
			try {
				const pdfjs = await import('pdfjs-dist');
				const workerSrc = (await import('pdfjs-dist/build/pdf.worker.min.mjs?url')).default;
				pdfjs.GlobalWorkerOptions.workerSrc = workerSrc;
				const doc = await pdfjs.getDocument({ url: source }).promise;
				if (cancelled) {
					void doc.destroy();
					return;
				}
				pdf = doc;
				const first = await doc.getPage(1);
				const size = first.getViewport({ scale: 1 });
				pageRatio = size.height / size.width;
				pageCount = doc.numPages;
				status = 'ready';
				await tick();
				if (!cancelled) observeFrames();
			} catch {
				if (!cancelled) status = 'error';
			}
		})();

		return () => {
			cancelled = true;
			for (const observer of observers) observer.disconnect();
			observers = [];
			renderedAt.clear();
			void pdf?.destroy();
			pdf = null;
			status = 'loading';
			pageCount = 0;
			currentPage = 1;
		};
	});

	$effect(() => {
		const el = scrollEl;
		if (!el) return;
		const update = () => {
			pageWidth = Math.max(260, Math.min(el.clientWidth - 48, PAGE_MAX_WIDTH));
		};
		update();
		const resize = new ResizeObserver(update);
		resize.observe(el);
		return () => resize.disconnect();
	});

	function zoomBy(delta: number) {
		const next = Math.min(ZOOM_STEPS.length - 1, Math.max(0, zoomIndex + delta));
		if (next === zoomIndex) return;
		zoomIndex = next;
		renderedAt.clear();
		void tick().then(() => {
			for (const frame of frames()) {
				const canvas = frame.querySelector('canvas');
				if (canvas && isVisible(frame)) void renderPage(canvas, Number(frame.dataset.page));
			}
		});
	}

	function isVisible(frame: HTMLDivElement) {
		const root = scrollEl;
		if (!root) return false;
		const top = frame.offsetTop;
		return (
			top < root.scrollTop + root.clientHeight + 800 &&
			top + frame.offsetHeight > root.scrollTop - 800
		);
	}

	// ---- Annotations -------------------------------------------------------------------------
	// Coordinates are stored in page-width units (x in 0..1, y in 0..pageRatio), so annotations
	// stay put at every zoom level and window size. They are saved in localStorage, per paper.
	type Tool = 'none' | 'pen' | 'highlight' | 'text' | 'eraser';
	type Point = [number, number];
	interface Stroke {
		id: string;
		page: number;
		kind: 'pen' | 'highlight';
		color: string;
		width: number;
		points: Point[];
	}
	interface Note {
		id: string;
		page: number;
		x: number;
		y: number;
		text: string;
		color: string;
	}

	const COLORS = [
		{ name: 'Red', value: '#ef4444' },
		{ name: 'Blue', value: '#2563eb' },
		{ name: 'Green', value: '#16a34a' },
		{ name: 'Yellow', value: '#facc15' },
		{ name: 'Black', value: '#111827' }
	];
	const PEN_WIDTH = 0.0032;
	const HIGHLIGHT_WIDTH = 0.02;
	const ERASE_RADIUS = 0.018;
	const NOTE_FONT = 0.0175;
	const HISTORY_LIMIT = 100;

	let tool = $state<Tool>('none');
	let color = $state(COLORS[0].value);
	let strokes = $state<Stroke[]>([]);
	let notes = $state<Note[]>([]);
	let draft = $state<Stroke | null>(null);
	let history = $state<string[]>([]);
	let erasing = false;
	let erasedSomething = false;
	let loadedKey: string | null = null;

	const storageKey = $derived(`trentorch:paper-annotations:v1:${url}`);
	const annotationCount = $derived(strokes.length + notes.length);
	const drawing = $derived(tool === 'pen' || tool === 'highlight');

	function snapshot(): string {
		return JSON.stringify({ strokes, notes });
	}

	function pushHistory() {
		history = [...history.slice(-(HISTORY_LIMIT - 1)), snapshot()];
	}

	function undo() {
		const previous = history.at(-1);
		if (previous === undefined) return;
		const parsed = parseAnnotations(previous);
		strokes = parsed.strokes;
		notes = parsed.notes;
		history = history.slice(0, -1);
	}

	function clearAll() {
		if (annotationCount === 0) return;
		if (!window.confirm('Remove all annotations on this paper?')) return;
		pushHistory();
		strokes = [];
		notes = [];
	}

	function isNumber(n: unknown): n is number {
		return typeof n === 'number' && Number.isFinite(n);
	}

	function isPoint(p: unknown): p is Point {
		return Array.isArray(p) && p.length === 2 && isNumber(p[0]) && isNumber(p[1]);
	}

	function parseAnnotations(raw: string | null): { strokes: Stroke[]; notes: Note[] } {
		const empty = { strokes: [] as Stroke[], notes: [] as Note[] };
		if (!raw) return empty;
		try {
			const data = JSON.parse(raw) as { strokes?: unknown; notes?: unknown };
			const loadedStrokes = (Array.isArray(data.strokes) ? data.strokes : []).filter(
				(s): s is Stroke =>
					!!s &&
					typeof s.id === 'string' &&
					isNumber(s.page) &&
					(s.kind === 'pen' || s.kind === 'highlight') &&
					typeof s.color === 'string' &&
					isNumber(s.width) &&
					Array.isArray(s.points) &&
					s.points.every(isPoint)
			);
			const loadedNotes = (Array.isArray(data.notes) ? data.notes : []).filter(
				(n): n is Note =>
					!!n &&
					typeof n.id === 'string' &&
					isNumber(n.page) &&
					isNumber(n.x) &&
					isNumber(n.y) &&
					typeof n.text === 'string' &&
					typeof n.color === 'string'
			);
			return { strokes: loadedStrokes, notes: loadedNotes };
		} catch {
			return empty;
		}
	}

	// Load when the paper changes, then save on every change. The load effect is declared first
	// so a new paper never overwrites its own saved annotations with the previous paper's.
	$effect(() => {
		const key = storageKey;
		if (!browser) return;
		let raw: string | null = null;
		try {
			raw = localStorage.getItem(key);
		} catch {
			// storage blocked (private mode): annotations simply won't persist
		}
		const parsed = parseAnnotations(raw);
		strokes = parsed.strokes;
		notes = parsed.notes;
		history = [];
		loadedKey = key;
	});

	$effect(() => {
		const key = storageKey;
		const payload = JSON.stringify({ v: 1, strokes, notes });
		if (!browser || loadedKey !== key) return;
		try {
			if (strokes.length + notes.length === 0) localStorage.removeItem(key);
			else localStorage.setItem(key, payload);
		} catch {
			// quota exceeded or storage blocked: keep working in memory
		}
	});

	function toPoint(event: MouseEvent, svg: SVGSVGElement): Point {
		const rect = svg.getBoundingClientRect();
		const x = Math.min(1, Math.max(0, (event.clientX - rect.left) / rect.width));
		const y = Math.min(pageRatio, Math.max(0, (event.clientY - rect.top) / rect.width));
		return [x, y];
	}

	function distanceToSegment(p: Point, a: Point, b: Point): number {
		const dx = b[0] - a[0];
		const dy = b[1] - a[1];
		const lengthSq = dx * dx + dy * dy;
		const t =
			lengthSq === 0
				? 0
				: Math.max(0, Math.min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / lengthSq));
		return Math.hypot(p[0] - (a[0] + t * dx), p[1] - (a[1] + t * dy));
	}

	function hitsStroke(stroke: Stroke, p: Point): boolean {
		const reach = ERASE_RADIUS + stroke.width / 2;
		if (stroke.points.length === 1) {
			return Math.hypot(p[0] - stroke.points[0][0], p[1] - stroke.points[0][1]) <= reach;
		}
		for (let i = 1; i < stroke.points.length; i++) {
			if (distanceToSegment(p, stroke.points[i - 1], stroke.points[i]) <= reach) return true;
		}
		return false;
	}

	function eraseAt(p: Point, page: number) {
		const keep = strokes.filter((stroke) => stroke.page !== page || !hitsStroke(stroke, p));
		if (keep.length === strokes.length) return;
		if (!erasedSomething) {
			pushHistory();
			erasedSomething = true;
		}
		strokes = keep;
	}

	function onPointerDown(event: PointerEvent, page: number) {
		if (tool === 'none') return;
		if (event.pointerType === 'mouse' && event.button !== 0) return;
		const svg = event.currentTarget as SVGSVGElement;
		const p = toPoint(event, svg);
		if (drawing) {
			svg.setPointerCapture(event.pointerId);
			draft = {
				id: crypto.randomUUID(),
				page,
				kind: tool === 'highlight' ? 'highlight' : 'pen',
				color,
				width: tool === 'highlight' ? HIGHLIGHT_WIDTH : PEN_WIDTH,
				points: [p, p]
			};
		} else if (tool === 'eraser') {
			svg.setPointerCapture(event.pointerId);
			erasing = true;
			erasedSomething = false;
			eraseAt(p, page);
		}
	}

	// Text notes are created on click (after the pointer is released): creating them on pointerdown
	// let the browser's default focus change steal focus from the new textarea, which then blurred
	// empty and deleted itself.
	function onClick(event: MouseEvent, page: number) {
		if (tool !== 'text') return;
		const p = toPoint(event, event.currentTarget as SVGSVGElement);
		const id = crypto.randomUUID();
		pushHistory();
		notes.push({
			id,
			page,
			x: Math.min(p[0], 0.9),
			y: Math.min(p[1], pageRatio - 0.03),
			text: '',
			color
		});
		void tick().then(() => document.getElementById(`note-${id}`)?.focus());
	}

	function onPointerMove(event: PointerEvent, page: number) {
		const svg = event.currentTarget as SVGSVGElement;
		if (draft && draft.page === page) {
			const p = toPoint(event, svg);
			const last = draft.points[draft.points.length - 1];
			if (Math.hypot(p[0] - last[0], p[1] - last[1]) > 0.0006) draft.points.push(p);
		} else if (erasing) {
			eraseAt(toPoint(event, svg), page);
		}
	}

	function onPointerUp() {
		if (draft) {
			pushHistory();
			strokes.push($state.snapshot(draft) as Stroke);
			draft = null;
		}
		erasing = false;
	}

	function strokePath(points: Point[]): string {
		return points
			.map((p, i) => `${i === 0 ? 'M' : 'L'}${p[0].toFixed(4)} ${p[1].toFixed(4)}`)
			.join(' ');
	}

	function removeNote(id: string) {
		pushHistory();
		notes = notes.filter((n) => n.id !== id);
	}

	function noteBlur(note: Note) {
		if (note.text.trim() === '') notes = notes.filter((n) => n.id !== note.id);
	}

	function noteCols(text: string): number {
		return Math.max(8, ...text.split('\n').map((line) => line.length + 1));
	}

	function noteRows(text: string): number {
		return text.split('\n').length;
	}

	const ARROW_STEP = 80;

	// Arrow keys, Page Up/Down, Home/End and Space scroll the paper when the viewer is the
	// thing being used. A plain scrollable div only does this while it has keyboard focus,
	// which clicking a canvas never gives it.
	function scrollViewerWithKey(event: KeyboardEvent): boolean {
		const el = scrollEl;
		if (!el || event.altKey || event.ctrlKey || event.metaKey) return false;
		const page = el.clientHeight * 0.9;
		switch (event.key) {
			case 'ArrowDown':
				el.scrollBy({ top: ARROW_STEP });
				return true;
			case 'ArrowUp':
				el.scrollBy({ top: -ARROW_STEP });
				return true;
			case 'ArrowRight':
				el.scrollBy({ left: ARROW_STEP });
				return true;
			case 'ArrowLeft':
				el.scrollBy({ left: -ARROW_STEP });
				return true;
			case 'PageDown':
				el.scrollBy({ top: page });
				return true;
			case 'PageUp':
				el.scrollBy({ top: -page });
				return true;
			case ' ':
				el.scrollBy({ top: event.shiftKey ? -page : page });
				return true;
			case 'Home':
				el.scrollTo({ top: 0 });
				return true;
			case 'End':
				el.scrollTo({ top: el.scrollHeight });
				return true;
			default:
				return false;
		}
	}

	function onWindowPointerDown(event: PointerEvent) {
		viewerActive = !!readerEl && event.target instanceof Node && readerEl.contains(event.target);
	}

	function onWindowKeydown(event: KeyboardEvent) {
		if (status !== 'ready') return;
		const target = event.target as HTMLElement | null;
		const typing =
			!!target &&
			(target.isContentEditable || ['INPUT', 'TEXTAREA', 'SELECT'].includes(target.tagName));
		if (typing) return;
		const inReader = !!target && !!readerEl && readerEl.contains(target);
		// Space on a focused button should still press it; arrows and paging never do.
		const onButton = !!target && ['BUTTON', 'A'].includes(target.tagName);
		if (
			(viewerActive || inReader) &&
			!(onButton && (event.key === ' ' || event.key === 'Enter')) &&
			!event.defaultPrevented &&
			scrollViewerWithKey(event)
		) {
			event.preventDefault();
			return;
		}
		if (event.key === 'Escape') {
			tool = 'none';
		} else if (
			(event.ctrlKey || event.metaKey) &&
			!event.shiftKey &&
			event.key.toLowerCase() === 'z'
		) {
			event.preventDefault();
			undo();
		}
	}

	const tools: { value: Tool; label: string; hint: string }[] = [
		{ value: 'none', label: 'Read', hint: 'Read and scroll (Esc)' },
		{ value: 'pen', label: 'Draw', hint: 'Freehand pen' },
		{ value: 'highlight', label: 'Highlight', hint: 'Highlighter' },
		{ value: 'text', label: 'Text', hint: 'Click the page to add text; click a note to edit it' },
		{
			value: 'eraser',
			label: 'Erase',
			hint: 'Drag over drawings, or click a text note, to remove it'
		}
	];
</script>

<svelte:window onkeydown={onWindowKeydown} onpointerdown={onWindowPointerDown} />

<section
	bind:this={readerEl}
	class="overflow-hidden rounded-2xl border border-white/10 bg-[#0b0b0d] shadow-2xl shadow-black/40"
	aria-label="Paper viewer for {title}"
>
	<div
		class="flex items-center justify-between gap-3 border-b border-white/10 bg-[#141417] px-4 py-2.5 text-xs text-white/70"
	>
		<div class="flex min-w-[5rem] items-center gap-1.5 font-mono tracking-wide">
			{#if status === 'ready'}
				<span class="text-white">{currentPage}</span>
				<span class="text-white/40">/ {pageCount}</span>
			{:else}
				<span class="text-white/40">{status === 'loading' ? 'Loading' : 'Unavailable'}</span>
			{/if}
		</div>
		<div class="flex items-center gap-1">
			<button
				type="button"
				onclick={() => zoomBy(-1)}
				disabled={zoomIndex === 0 || status !== 'ready'}
				aria-label="Zoom out"
				class="rounded-md p-1.5 transition-colors hover:bg-white/10 disabled:opacity-30"
			>
				<ZoomOut class="size-4" />
			</button>
			<span class="w-12 text-center font-mono text-white/60">{Math.round(scale * 100)}%</span>
			<button
				type="button"
				onclick={() => zoomBy(1)}
				disabled={zoomIndex === ZOOM_STEPS.length - 1 || status !== 'ready'}
				aria-label="Zoom in"
				class="rounded-md p-1.5 transition-colors hover:bg-white/10 disabled:opacity-30"
			>
				<ZoomIn class="size-4" />
			</button>
		</div>
		<!-- eslint-disable svelte/no-navigation-without-resolve -- external arXiv URL, not an app route -->
		<a
			href={fallbackHref}
			target="_blank"
			rel="noopener noreferrer"
			class="inline-flex min-w-[5rem] items-center justify-end gap-1 rounded-md px-2 py-1 transition-colors hover:bg-white/10 hover:text-white"
		>
			<ExternalLink class="size-3.5" />
			arXiv
		</a>
		<!-- eslint-enable svelte/no-navigation-without-resolve -->
	</div>

	{#if status === 'ready'}
		<div
			class="flex flex-wrap items-center gap-x-4 gap-y-2 border-b border-white/10 bg-[#101013] px-4 py-2 text-xs text-white/70"
			role="toolbar"
			aria-label="Annotation tools"
		>
			<div class="flex items-center gap-1">
				{#each tools as t (t.value)}
					<button
						type="button"
						onclick={() => (tool = t.value)}
						aria-pressed={tool === t.value}
						title={t.hint}
						class="inline-flex items-center gap-1.5 rounded-md px-2.5 py-1.5 transition-colors focus-visible:ring-2 focus-visible:ring-white/40 focus-visible:outline-none {tool ===
						t.value
							? 'bg-white text-black'
							: 'hover:bg-white/10 hover:text-white'}"
					>
						{#if t.value === 'none'}
							<Hand class="size-3.5" />
						{:else if t.value === 'pen'}
							<Pencil class="size-3.5" />
						{:else if t.value === 'highlight'}
							<Highlighter class="size-3.5" />
						{:else if t.value === 'text'}
							<Type class="size-3.5" />
						{:else}
							<Eraser class="size-3.5" />
						{/if}
						{t.label}
					</button>
				{/each}
			</div>

			<div class="flex items-center gap-1.5" role="group" aria-label="Annotation colour">
				{#each COLORS as c (c.value)}
					<button
						type="button"
						onclick={() => (color = c.value)}
						aria-pressed={color === c.value}
						aria-label={c.name}
						title={c.name}
						class="size-5 rounded-full border-2 transition-transform focus-visible:ring-2 focus-visible:ring-white/40 focus-visible:outline-none {color ===
						c.value
							? 'scale-110 border-white'
							: 'border-white/20 hover:scale-105'}"
						style="background-color: {c.value}"
					></button>
				{/each}
			</div>

			<div class="ml-auto flex items-center gap-1">
				<button
					type="button"
					onclick={undo}
					disabled={history.length === 0}
					title="Undo (Ctrl+Z)"
					class="inline-flex items-center gap-1.5 rounded-md px-2.5 py-1.5 transition-colors hover:bg-white/10 hover:text-white disabled:opacity-30"
				>
					<Undo2 class="size-3.5" /> Undo
				</button>
				<button
					type="button"
					onclick={clearAll}
					disabled={annotationCount === 0}
					title="Remove all annotations on this paper"
					class="inline-flex items-center gap-1.5 rounded-md px-2.5 py-1.5 transition-colors hover:bg-white/10 hover:text-white disabled:opacity-30"
				>
					<Trash class="size-3.5" /> Clear
				</button>
				<span class="ml-2 hidden text-white/40 sm:inline">Saved in this browser</span>
			</div>
		</div>
	{/if}

	<div
		bind:this={scrollEl}
		tabindex="-1"
		role="region"
		aria-label="Paper pages. Use the arrow keys to scroll."
		class="h-[78vh] overflow-y-auto px-4 py-6 outline-none"
	>
		{#if status === 'loading'}
			<div class="flex h-full items-center justify-center text-white/50">
				<Loader class="size-5 animate-spin" />
			</div>
		{:else if status === 'error'}
			<div class="flex h-full flex-col items-center justify-center gap-3 text-sm text-white/60">
				<p>This paper could not be rendered here.</p>
				<!-- eslint-disable svelte/no-navigation-without-resolve -- external arXiv URL, not an app route -->
				<a
					href={fallbackHref}
					target="_blank"
					rel="noopener noreferrer"
					class="underline underline-offset-4"
				>
					Open the PDF on arXiv
				</a>
				<!-- eslint-enable svelte/no-navigation-without-resolve -->
			</div>
		{:else}
			<div bind:this={pagesEl} class="mx-auto flex flex-col items-center gap-6">
				{#each pageNumbers as n (n)}
					<div
						data-page={n}
						class="relative overflow-hidden rounded-[2px] bg-white shadow-[0_18px_50px_-12px_rgba(0,0,0,0.8)]"
						style="width: {pageWidth * scale}px; height: {pageWidth * scale * pageRatio}px"
					>
						<canvas class="block"></canvas>
						<svg
							class="absolute inset-0 size-full {tool === 'none'
								? 'pointer-events-none'
								: tool === 'text'
									? 'cursor-text'
									: tool === 'eraser'
										? 'cursor-cell'
										: 'cursor-crosshair'}"
							style:touch-action={tool === 'none' ? 'auto' : 'none'}
							viewBox="0 0 1 {pageRatio}"
							preserveAspectRatio="none"
							aria-hidden="true"
							onpointerdown={(e) => onPointerDown(e, n)}
							onclick={(e) => onClick(e, n)}
							onpointermove={(e) => onPointerMove(e, n)}
							onpointerup={onPointerUp}
							onpointercancel={onPointerUp}
						>
							{#each strokes as stroke (stroke.id)}
								{#if stroke.page === n}
									<path
										d={strokePath(stroke.points)}
										fill="none"
										stroke={stroke.color}
										stroke-width={stroke.width}
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-opacity={stroke.kind === 'highlight' ? 0.4 : 1}
										style:mix-blend-mode={stroke.kind === 'highlight' ? 'multiply' : 'normal'}
									/>
								{/if}
							{/each}
							{#if draft && draft.page === n}
								<path
									d={strokePath(draft.points)}
									fill="none"
									stroke={draft.color}
									stroke-width={draft.width}
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-opacity={draft.kind === 'highlight' ? 0.4 : 1}
									style:mix-blend-mode={draft.kind === 'highlight' ? 'multiply' : 'normal'}
								/>
							{/if}
						</svg>
						{#each notes as note (note.id)}
							{#if note.page === n}
								<textarea
									id="note-{note.id}"
									bind:value={note.text}
									cols={noteCols(note.text)}
									rows={noteRows(note.text)}
									placeholder="Text"
									aria-label="Text annotation"
									spellcheck="false"
									onblur={() => noteBlur(note)}
									onclick={() => tool === 'eraser' && removeNote(note.id)}
									class="absolute resize-none overflow-hidden rounded-sm border border-transparent bg-transparent p-0.5 leading-tight whitespace-pre outline-none placeholder:text-black/30 {tool ===
									'text'
										? 'pointer-events-auto cursor-text border-dashed border-black/30 focus:border-black/50'
										: tool === 'eraser'
											? 'pointer-events-auto cursor-cell hover:bg-red-500/20'
											: 'pointer-events-none'}"
									style="left: {note.x * 100}%; top: {(note.y / pageRatio) *
										100}%; color: {note.color}; font-size: {NOTE_FONT * pageWidth * scale}px"
								></textarea>
							{/if}
						{/each}
					</div>
				{/each}
			</div>
		{/if}
	</div>
</section>
