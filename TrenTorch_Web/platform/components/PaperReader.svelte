<script lang="ts">
	import { browser } from '$app/environment';
	import { tick, untrack } from 'svelte';
	import { SvelteMap } from 'svelte/reactivity';
	import type { PDFDocumentProxy } from 'pdfjs-dist';
	import { ZoomIn, ZoomOut, ExternalLink, Loader } from '@lucide/svelte';

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
</script>

<section
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

	<div bind:this={scrollEl} class="h-[78vh] overflow-y-auto px-4 py-6">
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
						class="overflow-hidden rounded-[2px] bg-white shadow-[0_18px_50px_-12px_rgba(0,0,0,0.8)]"
						style="width: {pageWidth * scale}px; height: {pageWidth * scale * pageRatio}px"
					>
						<canvas class="block"></canvas>
					</div>
				{/each}
			</div>
		{/if}
	</div>
</section>
