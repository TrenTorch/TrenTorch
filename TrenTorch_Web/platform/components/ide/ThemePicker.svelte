<script lang="ts">
	import { Check, Minus, Palette, Plus } from '@lucide/svelte';
	import { EDITOR_FONT_DEFAULT, EDITOR_FONT_MAX, EDITOR_FONT_MIN } from './CodeEditor.svelte';
	import { IDE_THEMES } from './ide-themes';
	import { ideTheme } from './ide-theme.svelte';

	let { fontSize, onFontSize } = $props<{
		fontSize: number;
		onFontSize: (size: number) => void;
	}>();

	let open = $state(false);
	let root: HTMLDivElement | undefined = $state();

	function onWindowPointerDown(event: PointerEvent) {
		if (open && root && !root.contains(event.target as Node)) open = false;
	}

	function onWindowKeydown(event: KeyboardEvent) {
		if (open && event.key === 'Escape') open = false;
	}
</script>

<svelte:window onpointerdown={onWindowPointerDown} onkeydown={onWindowKeydown} />

<div class="relative" bind:this={root}>
	<button
		type="button"
		class="flex items-center gap-2 rounded-md p-2 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground {open
			? 'bg-muted text-foreground'
			: ''}"
		aria-haspopup="dialog"
		aria-expanded={open}
		title="Appearance: theme and text size"
		aria-label="Appearance: theme and text size"
		onclick={() => (open = !open)}
	>
		<Palette class="size-4" />
	</button>

	{#if open}
		<div
			role="dialog"
			aria-label="Appearance"
			class="theme-popover absolute top-full right-0 z-50 mt-2 w-[22rem] max-w-[calc(100vw-1.5rem)] rounded-lg border border-border bg-background p-3 shadow-2xl"
		>
			<p
				class="px-1 pb-2 text-[11px] font-semibold tracking-[0.12em] text-muted-foreground uppercase"
			>
				Colour theme
			</p>
			<div class="flex flex-col gap-1.5" role="radiogroup" aria-label="Colour theme">
				{#each IDE_THEMES as theme (theme.id)}
					{@const selected = ideTheme.id === theme.id}
					<button
						type="button"
						role="radio"
						aria-checked={selected}
						class="group flex items-center gap-3 rounded-md border p-2 text-left transition-colors {selected
							? 'border-(--ide-accent) bg-muted'
							: 'border-transparent hover:bg-muted/60'}"
						onclick={() => ideTheme.set(theme.id)}
					>
						<span
							class="flex h-11 w-16 shrink-0 flex-col justify-center gap-1 rounded-md border px-2"
							style:background={theme.ui.code}
							style:border-color={theme.ui.line}
							aria-hidden="true"
						>
							<span class="flex gap-1">
								<span class="h-1 w-3 rounded-full" style:background={theme.editor.keyword}></span>
								<span class="h-1 w-5 rounded-full" style:background={theme.editor.fn}></span>
							</span>
							<span class="flex gap-1 pl-2">
								<span class="h-1 w-4 rounded-full" style:background={theme.editor.string}></span>
								<span class="h-1 w-2 rounded-full" style:background={theme.editor.number}></span>
							</span>
							<span class="flex items-center gap-1">
								<span class="h-1 w-5 rounded-full" style:background={theme.editor.comment}></span>
								<span class="size-1.5 rounded-full" style:background={theme.ui.accent}></span>
							</span>
						</span>
						<span class="min-w-0 flex-1">
							<span class="block text-sm font-medium text-foreground">{theme.name}</span>
							<span class="block truncate text-xs text-muted-foreground">{theme.blurb}</span>
						</span>
						{#if selected}
							<Check class="size-4 shrink-0 text-(--ide-accent)" aria-hidden="true" />
						{/if}
					</button>
				{/each}
			</div>

			<div class="mt-3 flex items-center justify-between border-t border-border px-1 pt-3">
				<span class="text-[11px] font-semibold tracking-[0.12em] text-muted-foreground uppercase"
					>Editor text</span
				>
				<div class="flex items-center gap-1" role="group" aria-label="Editor font size">
					<button
						type="button"
						class="flex size-7 items-center justify-center rounded-md bg-muted text-foreground transition-colors hover:bg-foreground/15 disabled:opacity-30"
						onclick={() => onFontSize(Math.max(EDITOR_FONT_MIN, fontSize - 1))}
						disabled={fontSize <= EDITOR_FONT_MIN}
						aria-label="Decrease editor font size"
					>
						<Minus class="size-3.5" />
					</button>
					<button
						type="button"
						class="min-w-12 rounded-md px-2 py-1 text-center font-mono text-xs text-foreground tabular-nums transition-colors hover:bg-muted"
						onclick={() => onFontSize(EDITOR_FONT_DEFAULT)}
						title="Reset to default"
						aria-label="Reset editor font size"
					>
						{fontSize}px
					</button>
					<button
						type="button"
						class="flex size-7 items-center justify-center rounded-md bg-muted text-foreground transition-colors hover:bg-foreground/15 disabled:opacity-30"
						onclick={() => onFontSize(Math.min(EDITOR_FONT_MAX, fontSize + 1))}
						disabled={fontSize >= EDITOR_FONT_MAX}
						aria-label="Increase editor font size"
					>
						<Plus class="size-3.5" />
					</button>
				</div>
			</div>
		</div>
	{/if}
</div>

<style>
	.theme-popover {
		animation: popover-in 140ms ease-out;
		transform-origin: top right;
	}

	@keyframes popover-in {
		from {
			opacity: 0;
			transform: translateY(-4px) scale(0.98);
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.theme-popover {
			animation: none;
		}
	}
</style>
