<script lang="ts">
	import { mount, unmount, type Component } from 'svelte';
	import { resolve } from '$app/paths';
	import TheoryReader from '$components/TheoryReader.svelte';
	import WorkbookCheck from '$components/cuda/viz/_shared/WorkbookCheck.svelte';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();

	// Every figure lives in components/cuda/viz/<id>/View.svelte; the chapter markdown leaves a
	// <div class="cuda-viz" data-viz="VIZ-..."> where it belongs and it is mounted here after hydration.
	const views = import.meta.glob('/platform/components/cuda/viz/*/View.svelte');

	const diagrams: Record<string, () => Promise<{ default: Component }>> = {
		'gpu-data-flow': () => import('$components/cuda/diagrams/GpuDataFlow.svelte'),
		'cpu-gpu-system': () => import('$components/cuda/diagrams/CpuGpuSystem.svelte'),
		'grid-of-blocks': () => import('$components/cuda/diagrams/GridOfBlocks.svelte'),
		'block-scheduling': () => import('$components/cuda/diagrams/BlockScheduling.svelte'),
		'warps-in-block': () => import('$components/cuda/diagrams/WarpsInBlock.svelte'),
		'chip-hierarchy': () => import('$components/cuda/diagrams/ChipHierarchy.svelte')
	};

	function mountFigures(root: HTMLElement) {
		const mounted: Record<string, unknown>[] = [];
		let cancelled = false;
		for (const el of root.querySelectorAll<HTMLElement>('.cuda-viz[data-viz]')) {
			const id = (el.dataset.viz ?? '').replace(/^VIZ-/, '').toLowerCase();
			const load = views[`/platform/components/cuda/viz/${id}/View.svelte`];
			if (!load) {
				el.innerHTML = `<p class="viz-pending">This interactive figure (${el.dataset.title ?? id}) is not built yet.</p>`;
				continue;
			}
			void load().then((mod) => {
				if (cancelled) return;
				mounted.push(
					mount((mod as { default: Component<{ mode: string; title: string }> }).default, {
						target: el,
						props: { mode: el.dataset.mode ?? '', title: el.dataset.title ?? '' }
					})
				);
			});
		}
		for (const el of root.querySelectorAll<HTMLElement>('.cuda-diagram[data-diagram]')) {
			const load = diagrams[el.dataset.diagram ?? ''];
			if (!load) continue;
			void load().then((mod) => {
				if (!cancelled) mounted.push(mount(mod.default, { target: el }));
			});
		}
		for (const el of root.querySelectorAll<HTMLElement>('.g1-check[data-problem]')) {
			mounted.push(
				mount(WorkbookCheck, { target: el, props: { problem: Number(el.dataset.problem) } })
			);
		}
		return () => {
			cancelled = true;
			for (const c of mounted) unmount(c);
		};
	}
</script>

<TheoryReader
	theory={data.theory}
	backHref={resolve('/cuda/theory')}
	backLabel="CUDA course"
	titlePrefix={data.chapter?.id}
	meta={data.meta}
	enhance={mountFigures}
/>

<nav class="mx-auto flex w-full max-w-[96rem] justify-between px-4 pb-10 text-sm lg:px-8">
	{#if data.prev}
		<a class="hover:underline" href={resolve('/cuda/theory/[chapter]', { chapter: data.prev.step })}
			>← {data.prev.id}: {data.prev.title}</a
		>
	{:else}<span></span>{/if}
	{#if data.next}
		<a class="hover:underline" href={resolve('/cuda/theory/[chapter]', { chapter: data.next.step })}
			>{data.next.id}: {data.next.title} →</a
		>
	{/if}
</nav>
