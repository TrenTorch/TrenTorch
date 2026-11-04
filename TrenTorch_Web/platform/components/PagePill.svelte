<script lang="ts">
	import { resolve } from '$app/paths';
	import WindowDots from './WindowDots.svelte';
	import { recent, type RecentArea } from '$processes/progress-tracking/recent.svelte';
	import { solved } from '$processes/progress-tracking/solved.svelte';

	// The small editor-window label at the top of a page's header: the three dots and where you are, as a
	// folder ("papers/"). It says what the page is without a second heading. Red goes home. Yellow is grey: the
	// page already fills the whole window, like a macOS app in a space of its own, so there is nothing to
	// minimise. Green picks up where the student left off in this area (the last question opened and not yet
	// solved, or the last paper read), and is grey when there is nowhere to pick up.
	let {
		slug,
		area,
		resume: given
	}: {
		slug: string;
		area: RecentArea;
		/** Where green goes, for a page that works that out itself (null: nowhere). */
		resume?: { label: string; href: string } | null;
	} = $props();

	const resume = $derived.by(() => {
		if (given !== undefined) return given;
		const last = recent.get(area);
		if (!last) return null;
		if (area === 'paper')
			return { label: 'last paper', href: resolve('/papers/[slug]', { slug: last }) };
		if (solved.isSolved(last)) return null;
		return { label: 'resume question', href: resolve('/ide/[id]', { id: last }) };
	});
</script>

<div
	class="mb-4 inline-flex items-center gap-3 rounded-full border border-border bg-secondary/50 py-1.5 pr-4 pl-3 font-mono text-xs text-muted-foreground"
>
	<WindowDots
		red={{ label: 'home', href: resolve('/') }}
		green={resume ? { label: resume.label, href: resume.href } : undefined}
	/>
	{slug}
</div>
