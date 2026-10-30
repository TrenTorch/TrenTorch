<script lang="ts">
	import {
		Building2,
		Check,
		Circle,
		CircleDot,
		RotateCcw,
		Search,
		SlidersHorizontal,
		X
	} from '@lucide/svelte';
	import { tick } from 'svelte';
	import { getPartIcon } from '$data/part-icons';

	type Module = { id: string; title: string; learningPartId: string };
	type Choice = { value: string; label: string; count: number };
	type Status = { value: string; label: string };
	type Facet = { key: string; name: string; value: string; clear: () => void };

	// The search box and every filter the popover edits. The page owns them so it can do the filtering.
	let {
		query = $bindable(''),
		moduleId = $bindable(''),
		topic = $bindable(''),
		company = $bindable(''),
		difficulty = $bindable(''),
		status = $bindable('all'),
		pastPotd = $bindable(),
		companyCases = $bindable(),
		modules = [],
		topics = [],
		companies = [],
		difficulties,
		statuses,
		resultCount,
		placeholder = 'Search problems...',
		noun = 'problem'
	}: {
		query?: string;
		moduleId?: string;
		topic?: string;
		company?: string;
		difficulty?: string;
		status?: string;
		/** Leave it out and the popover has no Past Problem of the Day switch. */
		pastPotd?: boolean;
		companyCases?: boolean;
		/** Module, topic and company are sections only when they have options. */
		modules?: Module[];
		topics?: Choice[];
		companies?: Choice[];
		difficulties: string[];
		statuses: Status[];
		resultCount: number;
		placeholder?: string;
		/** What is being counted, singular: "problem", "question". */
		noun?: string;
	} = $props();

	let open = $state(false);
	let topicSearch = $state('');
	let companySearch = $state('');
	let root = $state<HTMLDivElement>();
	let trigger = $state<HTMLButtonElement>();
	let searchInput = $state<HTMLInputElement>();
	let searchFocused = $state(false);

	// What is applied, as removable chips under the bar. The search text is not one: it is right there in the box.
	const applied = $derived.by(() => {
		const list: Facet[] = [];
		if (moduleId) {
			list.push({
				key: 'module',
				name: 'Module',
				value: modules.find((m) => m.id === moduleId)?.title ?? moduleId,
				clear: () => (moduleId = '')
			});
		}
		if (topic) {
			list.push({
				key: 'topic',
				name: 'Topic',
				value: topics.find((t) => t.value === topic)?.label ?? topic,
				clear: () => (topic = '')
			});
		}
		if (company) {
			list.push({ key: 'company', name: 'Company', value: company, clear: () => (company = '') });
		}
		if (difficulty) {
			list.push({
				key: 'difficulty',
				name: 'Difficulty',
				value: difficulty,
				clear: () => (difficulty = '')
			});
		}
		if (status !== 'all') {
			list.push({
				key: 'status',
				name: 'Status',
				value: statuses.find((s) => s.value === status)?.label ?? status,
				clear: () => (status = 'all')
			});
		}
		if (pastPotd) {
			list.push({ key: 'potd', name: 'Only', value: 'Past POTD', clear: () => (pastPotd = false) });
		}
		if (companyCases) {
			list.push({ key: 'company-cases', name: 'Only', value: 'Company Case Studies', clear: () => (companyCases = false) });
		}
		return list;
	});

	const shownTopics = $derived(
		topics.filter((t) => t.label.toLowerCase().includes(topicSearch.trim().toLowerCase()))
	);
	const shownCompanies = $derived(
		companies.filter((c) => c.label.toLowerCase().includes(companySearch.trim().toLowerCase()))
	);

	// Fades the bottom edge of a scrolling chip list while there is more below it.
	function fadeWhenMore(node: HTMLElement) {
		const update = () =>
			node.classList.toggle('more', node.scrollHeight - node.scrollTop - node.clientHeight > 4);
		node.addEventListener('scroll', update, { passive: true });
		const resize = new ResizeObserver(update);
		resize.observe(node);
		const mutate = new MutationObserver(update);
		mutate.observe(node, { childList: true, subtree: true });
		update();
		return {
			destroy() {
				node.removeEventListener('scroll', update);
				resize.disconnect();
				mutate.disconnect();
			}
		};
	}

	// A popover that opens near the bottom of a short screen would run off it; bring it into view.
	async function keepInView() {
		await tick();
		const box = root?.querySelector('.popover')?.getBoundingClientRect();
		if (box && box.bottom > window.innerHeight - 12) {
			window.scrollBy({ top: box.bottom - window.innerHeight + 20, behavior: 'smooth' });
		}
	}

	function reset() {
		moduleId = '';
		topic = '';
		company = '';
		difficulty = '';
		status = 'all';
		if (pastPotd !== undefined) pastPotd = false;
		companyCases = false;
	}

	function close(returnFocus = false) {
		open = false;
		topicSearch = '';
		companySearch = '';
		if (returnFocus) trigger?.focus();
	}

	function onPointerDown(event: PointerEvent) {
		if (open && root && !root.contains(event.target as Node)) close();
	}

	function onKeydown(event: KeyboardEvent) {
		if (event.key === 'Escape' && open) {
			close(true);
			return;
		}
		// "/" jumps to the search box, as on GitHub and most docs sites, unless the user is already typing.
		if (event.key !== '/' || event.metaKey || event.ctrlKey || event.altKey) return;
		const el = event.target as HTMLElement;
		if (el.closest('input, textarea, select, [contenteditable="true"]')) return;
		event.preventDefault();
		searchInput?.focus();
	}
</script>

<svelte:window onpointerdown={onPointerDown} onkeydown={onKeydown} />

<div class="bar">
	<label class="search">
		<span class="sr-only">{placeholder.replace(/\.+$/, '')}</span>
		<Search class="search-icon" aria-hidden="true" />
		<input
			bind:this={searchInput}
			bind:value={query}
			onfocus={() => (searchFocused = true)}
			onblur={() => (searchFocused = false)}
			type="search"
			{placeholder}
		/>
		{#if !query && !searchFocused}
			<kbd class="search-key" aria-hidden="true">/</kbd>
		{/if}
	</label>

	<div class="relative" bind:this={root}>
		<button
			bind:this={trigger}
			type="button"
			class="trigger press {open || applied.length ? 'on' : ''}"
			aria-haspopup="dialog"
			aria-expanded={open}
			onclick={() => {
				if (open) close();
				else {
					open = true;
					keepInView();
				}
			}}
		>
			<SlidersHorizontal class="size-4" aria-hidden="true" />
			<span>Filters</span>
			{#if applied.length}
				<span class="trigger-count" aria-label="{applied.length} active">{applied.length}</span>
			{/if}
		</button>

		{#if open}
			<button
				type="button"
				class="scrim"
				tabindex="-1"
				aria-label="Close filters"
				onclick={() => close()}
			></button>
			<div role="dialog" aria-label="Filters" class="popover">
				<div class="pop-head">
					<span class="dots" aria-hidden="true"><i></i><i></i><i></i></span>
					<span class="pop-title">filters</span>
					<span class="pop-meta">{applied.length ? `${applied.length} active` : 'none active'}</span
					>
					{#if applied.length}
						<button type="button" class="pop-reset" onclick={reset}>
							<RotateCcw class="size-3" aria-hidden="true" />
							reset
						</button>
					{/if}
					<button
						type="button"
						class="pop-x"
						aria-label="Close filters"
						onclick={() => close(true)}
					>
						<X class="size-4" aria-hidden="true" />
					</button>
				</div>

				<div class="pop-body">
					{#if modules.length}
						<section aria-labelledby="f-module">
							<h3 id="f-module" class="label">Module</h3>
							<div class="chips">
								{#each modules as m (m.id)}
									{@const Icon = getPartIcon(m.learningPartId)}
									<button
										type="button"
										class="chip {moduleId === m.id ? 'selected' : ''}"
										aria-pressed={moduleId === m.id}
										onclick={() => (moduleId = moduleId === m.id ? '' : m.id)}
									>
										<Icon class="size-3.5" aria-hidden="true" />
										{m.title}
									</button>
								{/each}
							</div>
						</section>
					{/if}

					<div class="rows">
						<section aria-labelledby="f-difficulty">
							<h3 id="f-difficulty" class="label">Difficulty</h3>
							<div class="chips">
								{#each difficulties as d (d)}
									<button
										type="button"
										class="chip level {d} {difficulty === d ? 'selected' : ''}"
										aria-pressed={difficulty === d}
										onclick={() => (difficulty = difficulty === d ? '' : d)}
									>
										<span class="level-dot" aria-hidden="true"></span>
										{d}
									</button>
								{/each}
							</div>
						</section>

						<section aria-labelledby="f-status">
							<h3 id="f-status" class="label">Status</h3>
							<div class="chips">
								{#each statuses.filter((s) => s.value !== 'all') as s (s.value)}
									<button
										type="button"
										class="chip {status === s.value ? 'selected' : ''}"
										aria-pressed={status === s.value}
										onclick={() => (status = status === s.value ? 'all' : s.value)}
									>
										{#if s.value === 'solved'}
											<Check class="size-3.5 text-[#3fb950]" aria-hidden="true" />
										{:else if s.value === 'attempted'}
											<CircleDot class="size-3.5 text-[#d29922]" aria-hidden="true" />
										{:else}
											<Circle class="size-3.5 text-muted-foreground" aria-hidden="true" />
										{/if}
										{s.label}
									</button>
								{/each}
							</div>
						</section>
					</div>

					{#if topics.length}
						<section aria-labelledby="f-topic">
							<div class="label-row">
								<h3 id="f-topic" class="label">
									Topic <span class="label-n">{topics.length}</span>
								</h3>
								<label class="mini">
									<Search class="mini-icon" aria-hidden="true" />
									<input
										bind:value={topicSearch}
										type="search"
										placeholder="Find a topic..."
										aria-label="Find a topic"
									/>
								</label>
							</div>
							<div class="chips scroll" use:fadeWhenMore>
								{#each shownTopics as t (t.value)}
									<button
										type="button"
										class="chip {topic === t.value ? 'selected' : ''}"
										aria-pressed={topic === t.value}
										onclick={() => (topic = topic === t.value ? '' : t.value)}
									>
										{t.label}
										<span class="chip-n">{t.count}</span>
									</button>
								{:else}
									<p class="none">No topic matches "{topicSearch}".</p>
								{/each}
							</div>
						</section>
					{/if}

					{#if companies.length}
						<section aria-labelledby="f-company">
							<div class="label-row">
								<h3 id="f-company" class="label">
									Company <span class="label-n">{companies.length}</span>
								</h3>
								<label class="mini">
									<Search class="mini-icon" aria-hidden="true" />
									<input
										bind:value={companySearch}
										type="search"
										placeholder="Find a company..."
										aria-label="Find a company"
									/>
								</label>
							</div>
							<div class="chips scroll" use:fadeWhenMore>
								{#each shownCompanies as c (c.value)}
									<button
										type="button"
										class="chip {company === c.value ? 'selected' : ''}"
										aria-pressed={company === c.value}
										onclick={() => (company = company === c.value ? '' : c.value)}
									>
										<Building2 class="size-3.5" aria-hidden="true" />
										{c.label}
										<span class="chip-n">{c.count}</span>
									</button>
								{:else}
									<p class="none">No company matches "{companySearch}".</p>
								{/each}
							</div>
						</section>
					{/if}
				</div>

				<div class="pop-foot">
					<div class="pop-foot-switches">
						{#if companyCases !== undefined}
						<button
							type="button"
							class="switch-row"
							role="switch"
							aria-checked={companyCases}
							onclick={() => (companyCases = !companyCases)}
						>
							<span class="switch {companyCases ? 'on' : ''}" aria-hidden="true"><span></span></span>
							<span class="switch-text">
								Company Case Studies
								<small>Company-labelled case-study questions</small>
							</span>
						</button>
					{/if}
					{#if pastPotd !== undefined}
							<button
								type="button"
								class="switch-row"
								role="switch"
								aria-checked={pastPotd}
								onclick={() => (pastPotd = !pastPotd)}
							>
								<span class="switch {pastPotd ? 'on' : ''}" aria-hidden="true"><span></span></span>
								<span class="switch-text">
									Past Problem of the Day
									<small>Featured on an earlier day</small>
								</span>
							</button>
						{/if}
					</div>
					<button type="button" class="show press" onclick={() => close(true)}>
						Show {resultCount}
						{resultCount === 1 ? noun : `${noun}s`}
					</button>
				</div>
			</div>
		{/if}
	</div>
</div>

{#if applied.length}
	<div class="applied" role="group" aria-label="Active filters">
		{#each applied as facet (facet.key)}
			<button
				type="button"
				class="applied-chip"
				aria-label="Remove {facet.name} filter: {facet.value}"
				onclick={facet.clear}
			>
				<span class="applied-name">{facet.name}</span>
				{facet.value}
				<X class="size-3" aria-hidden="true" />
			</button>
		{/each}
		<button type="button" class="applied-clear" onclick={reset}>Clear all</button>
	</div>
{/if}

<p class="result-line" aria-live="polite">
	<span>{resultCount}</span>
	{resultCount === 1 ? noun : `${noun}s`}
</p>

<style>
	.bar {
		display: flex;
		align-items: center;
		gap: 8px;
		margin-bottom: 10px;
	}

	/* The search box and the Filters button share one height, radius and border, so they read as one bar. */
	.search {
		position: relative;
		min-width: 0;
		flex: 1;
	}

	.search input {
		width: 100%;
		height: 42px;
		border: 1px solid var(--border);
		border-radius: 10px;
		background: var(--secondary);
		padding: 0 40px 0 38px;
		color: var(--foreground);
		font: inherit;
		font-size: 0.85rem;
		transition:
			border-color 150ms,
			box-shadow 150ms;
	}

	.search input::placeholder {
		color: var(--muted-foreground);
	}

	.search input:focus {
		border-color: var(--primary);
		box-shadow: 0 0 0 3px color-mix(in srgb, var(--primary) 16%, transparent);
		outline: none;
	}

	.search :global(.search-icon) {
		position: absolute;
		top: 50%;
		left: 13px;
		width: 16px;
		height: 16px;
		transform: translateY(-50%);
		color: var(--muted-foreground);
		pointer-events: none;
	}

	.search-key {
		position: absolute;
		top: 50%;
		right: 11px;
		transform: translateY(-50%);
		border: 1px solid var(--border);
		border-bottom-width: 2px;
		border-radius: 5px;
		background: var(--background);
		padding: 1px 7px;
		color: var(--muted-foreground);
		font-family: var(--font-mono);
		font-size: 0.72rem;
		pointer-events: none;
	}

	/* A keyboard hint means nothing on a touch screen. */
	@media (hover: none) {
		.search-key {
			display: none;
		}
	}

	.trigger {
		display: inline-flex;
		height: 42px;
		align-items: center;
		gap: 8px;
		border: 1px solid var(--border);
		border-radius: 10px;
		background: var(--secondary);
		padding: 0 14px;
		color: var(--foreground);
		font-family: var(--font-mono);
		font-size: 0.74rem;
		font-weight: 500;
		letter-spacing: 0.07em;
		text-transform: uppercase;
		cursor: pointer;
		transition:
			border-color 150ms,
			background 150ms;
	}

	.trigger:hover {
		background: var(--muted);
	}

	.trigger.on {
		border-color: color-mix(in srgb, var(--primary) 55%, var(--border));
	}

	.trigger-count {
		display: inline-flex;
		min-width: 19px;
		height: 19px;
		align-items: center;
		justify-content: center;
		border-radius: 999px;
		background: var(--primary);
		padding: 0 5px;
		color: var(--primary-foreground);
		font-size: 0.68rem;
		letter-spacing: 0;
	}

	.scrim {
		display: none;
	}

	.popover {
		position: absolute;
		z-index: 40;
		top: calc(100% + 8px);
		right: 0;
		display: flex;
		width: min(480px, calc(100vw - 32px));
		flex-direction: column;
		overflow: hidden;
		border: 1px solid var(--border);
		border-radius: 14px;
		background: var(--popover);
		box-shadow:
			0 18px 50px -12px rgb(0 0 0 / 28%),
			0 2px 6px rgb(0 0 0 / 6%);
		animation: pop-in 140ms ease-out;
	}

	@keyframes pop-in {
		from {
			opacity: 0;
			transform: translateY(-6px) scale(0.985);
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.popover {
			animation: none;
		}
	}

	/* The window chrome from the home page's code card, small. */
	.pop-head {
		display: flex;
		align-items: center;
		gap: 10px;
		border-bottom: 1px solid var(--border);
		background: var(--secondary);
		padding: 10px 12px 10px 14px;
		font-family: var(--font-mono);
		font-size: 0.72rem;
	}

	.dots {
		display: inline-flex;
		gap: 6px;
	}

	.dots i {
		display: block;
		width: 9px;
		height: 9px;
		border-radius: 50%;
	}

	.dots i:nth-child(1) {
		background: #ff5f57;
	}

	.dots i:nth-child(2) {
		background: #febc2e;
	}

	.dots i:nth-child(3) {
		background: #28c840;
	}

	.pop-title {
		color: var(--foreground);
	}

	.pop-meta {
		margin-right: auto;
		color: var(--muted-foreground);
	}

	.pop-reset {
		display: inline-flex;
		align-items: center;
		gap: 5px;
		border: 0;
		background: transparent;
		padding: 3px 6px;
		/* The dark theme's brand red is deep; mixed toward the text colour it stays readable on both. */
		color: color-mix(in srgb, var(--primary) 60%, var(--foreground));
		font: inherit;
		cursor: pointer;
	}

	.pop-reset:hover {
		text-decoration: underline;
	}

	.pop-x {
		display: inline-flex;
		align-items: center;
		border: 0;
		border-radius: 6px;
		background: transparent;
		padding: 3px;
		color: var(--muted-foreground);
		cursor: pointer;
	}

	.pop-x:hover {
		background: var(--muted);
		color: var(--foreground);
	}

	.pop-body {
		display: flex;
		max-height: min(60vh, 540px);
		flex-direction: column;
		gap: 18px;
		overflow-y: auto;
		padding: 16px 16px 14px;
	}

	.rows {
		display: flex;
		flex-direction: column;
		gap: 18px;
	}

	.label {
		margin: 0 0 8px;
		color: var(--muted-foreground);
		font-family: var(--font-mono);
		font-size: 0.68rem;
		font-weight: 500;
		letter-spacing: 0.1em;
		text-transform: uppercase;
	}

	.label-n {
		margin-left: 4px;
		color: color-mix(in srgb, var(--muted-foreground) 70%, transparent);
	}

	.label-row {
		display: flex;
		align-items: baseline;
		justify-content: space-between;
		gap: 12px;
		margin-bottom: 8px;
	}

	.label-row .label {
		margin: 0;
	}

	.mini {
		position: relative;
		display: block;
		width: 168px;
	}

	.mini input {
		width: 100%;
		height: 28px;
		border: 1px solid var(--border);
		border-radius: 8px;
		background: var(--background);
		padding: 0 8px 0 27px;
		color: var(--foreground);
		font: inherit;
		font-size: 0.74rem;
		transition: border-color 150ms;
	}

	.mini input:focus {
		border-color: var(--primary);
		outline: none;
	}

	.mini :global(.mini-icon) {
		position: absolute;
		top: 50%;
		left: 9px;
		width: 12px;
		height: 12px;
		transform: translateY(-50%);
		color: var(--muted-foreground);
		pointer-events: none;
	}

	.chips {
		display: flex;
		flex-wrap: wrap;
		gap: 6px;
	}

	.chips.scroll.more {
		-webkit-mask-image: linear-gradient(to bottom, #000 calc(100% - 26px), transparent);
		mask-image: linear-gradient(to bottom, #000 calc(100% - 26px), transparent);
	}

	.chips.scroll {
		max-height: 112px;
		align-content: flex-start;
		overflow-y: auto;
		padding-right: 4px;
	}

	.chip {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		border: 1px solid var(--border);
		border-radius: 999px;
		background: var(--background);
		padding: 5px 11px;
		color: var(--foreground);
		font: inherit;
		font-size: 0.76rem;
		white-space: nowrap;
		cursor: pointer;
		transition:
			border-color 120ms,
			background 120ms,
			color 120ms;
	}

	.chip:hover {
		border-color: color-mix(in srgb, var(--primary) 45%, var(--border));
		background: var(--muted);
	}

	/* The brand tint the old topic pills used for their selected state. */
	.chip.selected {
		border-color: var(--primary);
		background: color-mix(in srgb, var(--primary) 13%, var(--background));
		color: color-mix(in srgb, var(--primary) 60%, var(--foreground));
	}

	.chip-n {
		color: var(--muted-foreground);
		font-family: var(--font-mono);
		font-size: 0.68rem;
	}

	/* Same colours as the difficulty badges in the table. */
	.level-dot {
		width: 7px;
		height: 7px;
		border-radius: 50%;
		background: var(--muted-foreground);
	}

	.level.Beginner .level-dot {
		background: #3fb950;
	}

	.level.Intermediate .level-dot {
		background: #d29922;
	}

	.level.Advanced .level-dot {
		background: #e5534b;
	}

	.level.Beginner.selected {
		border-color: #3fb950;
		background: rgb(63 185 80 / 12%);
		color: color-mix(in srgb, #3fb950 70%, var(--foreground));
	}

	.level.Intermediate.selected {
		border-color: #d29922;
		background: rgb(210 153 34 / 12%);
		color: color-mix(in srgb, #d29922 70%, var(--foreground));
	}

	.level.Advanced.selected {
		border-color: #e5534b;
		background: rgb(229 83 75 / 12%);
		color: color-mix(in srgb, #e5534b 75%, var(--foreground));
	}

	.none {
		margin: 4px 0;
		color: var(--muted-foreground);
		font-size: 0.76rem;
	}

	.pop-foot {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 14px;
		border-top: 1px solid var(--border);
		background: var(--secondary);
		padding: 12px 14px;
	}

	.pop-foot-switches {
		display: flex;
		align-items: center;
		gap: 14px;
		min-width: 0;
	}

	.switch-row {
		display: flex;
		min-width: 0;
		align-items: center;
		gap: 10px;
		border: 0;
		background: transparent;
		padding: 0;
		color: var(--foreground);
		font: inherit;
		text-align: left;
		cursor: pointer;
	}

	.switch {
		position: relative;
		flex: none;
		width: 34px;
		height: 20px;
		border: 1px solid var(--border);
		border-radius: 999px;
		background: var(--muted);
		transition:
			background 150ms,
			border-color 150ms;
	}

	.switch span {
		position: absolute;
		top: 2px;
		left: 2px;
		width: 14px;
		height: 14px;
		border-radius: 50%;
		background: var(--muted-foreground);
		transition:
			transform 150ms,
			background 150ms;
	}

	.switch.on {
		border-color: var(--primary);
		background: color-mix(in srgb, var(--primary) 25%, var(--background));
	}

	.switch.on span {
		transform: translateX(14px);
		background: var(--primary);
	}

	.switch-text {
		display: flex;
		flex-direction: column;
		font-size: 0.78rem;
		font-weight: 500;
	}

	.switch-text small {
		margin-top: 1px;
		color: var(--muted-foreground);
		font-size: 0.68rem;
		font-weight: 400;
		line-height: 1.3;
	}

	.show {
		flex: none;
		margin-left: auto;
		border: 0;
		border-radius: 9px;
		background: var(--primary);
		padding: 9px 16px;
		color: var(--primary-foreground);
		font-size: 0.78rem;
		font-weight: 500;
		white-space: nowrap;
		cursor: pointer;
		transition: filter 150ms;
	}

	.show:hover {
		filter: brightness(1.1);
	}

	.applied {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 6px;
		margin-bottom: 10px;
	}

	.applied-chip {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		border: 1px solid color-mix(in srgb, var(--primary) 35%, var(--border));
		border-radius: 999px;
		background: color-mix(in srgb, var(--primary) 9%, var(--background));
		padding: 3px 9px 3px 4px;
		color: color-mix(in srgb, var(--primary) 55%, var(--foreground));
		font: inherit;
		font-size: 0.74rem;
		cursor: pointer;
		transition: border-color 120ms;
	}

	.applied-chip:hover {
		border-color: var(--primary);
	}

	.applied-name {
		border-radius: 999px;
		background: color-mix(in srgb, var(--primary) 16%, var(--background));
		padding: 1px 7px;
		font-family: var(--font-mono);
		font-size: 0.64rem;
		letter-spacing: 0.06em;
		text-transform: uppercase;
	}

	.applied-clear {
		border: 0;
		background: transparent;
		padding: 3px 6px;
		color: var(--muted-foreground);
		font: inherit;
		font-size: 0.74rem;
		text-decoration: underline;
		text-underline-offset: 3px;
		cursor: pointer;
	}

	.applied-clear:hover {
		color: var(--foreground);
	}

	.result-line {
		margin: 0 0 8px;
		color: var(--muted-foreground);
		font-family: var(--font-mono);
		font-size: 0.72rem;
		letter-spacing: 0.04em;
	}

	.result-line span {
		color: var(--foreground);
		font-weight: 600;
	}

	/* Phones, and any screen too short for the popover to hang under its button (a phone on its side):
	   the popover becomes a sheet at the bottom of the screen. */
	@media (max-width: 640px), (max-height: 560px) {
		.scrim {
			position: fixed;
			z-index: 39;
			inset: 0;
			display: block;
			border: 0;
			background: rgb(0 0 0 / 40%);
		}

		.popover {
			position: fixed;
			z-index: 40;
			inset: auto 8px 8px;
			width: auto;
			max-width: 560px;
			margin-inline: auto;
			/* Never taller than what is visible below the navbar (57px, sticky) plus a 16px gap above and the
			   8px inset below, and never more than 640px, so some of the page always shows behind it.
			   dvh is the visible height; plain vh is the tall one that ignores the browser's toolbar. */
			max-height: min(calc(100vh - 81px), 640px);
			max-height: min(calc(100dvh - 81px), 640px);
			animation-name: sheet-in;
		}

		.pop-body {
			max-height: none;
			flex: 1;
		}
	}

	@media (max-width: 640px) {
		.pop-foot {
			flex-direction: column;
			align-items: stretch;
		}

		/* Stacked under the switch, the button fills the width instead of sitting to the right. */
		.show {
			margin-left: 0;
		}
	}

	@keyframes sheet-in {
		from {
			opacity: 0;
			transform: translateY(14px);
		}
	}
</style>
