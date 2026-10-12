<script lang="ts">
	import * as Dialog from '$components/ui/dialog';
	import { Textarea } from '$components/ui/textarea';
	import { Input } from '$components/ui/input';
	import Button from '../Button.svelte';
	import { page } from '$app/state';
	import { browser } from '$app/environment';
	import { PUBLIC_BUG_REPORT_TURNSTILE_SITE_KEY } from '$env/static/public';
	import { CheckCircle2 } from '@lucide/svelte';

	interface TurnstileGlobal {
		render: (
			container: HTMLElement,
			options: {
				sitekey: string;
				callback: (token: string) => void;
				'expired-callback': () => void;
				'error-callback': () => void;
			}
		) => string;
		reset: (widgetId: string) => void;
	}

	let {
		open = $bindable(false),
		questionId,
		questionTitle
	}: {
		open?: boolean;
		questionId: string;
		questionTitle: string;
	} = $props();

	let whatIsWrong = $state('');
	let profile = $state('');
	let correction = $state('');
	let turnstileToken = $state('');
	let turnstileContainer: HTMLDivElement | undefined = $state();
	let turnstileWidgetId: string | undefined;
	let isSubmitting = $state(false);
	let submitError = $state<string | null>(null);
	let issueUrl = $state<string | null>(null);

	function resetForm() {
		whatIsWrong = '';
		profile = '';
		correction = '';
		turnstileToken = '';
		isSubmitting = false;
		submitError = null;
		issueUrl = null;
	}

	// Loaded once per dialog open rather than globally, so the widget's
	// lifetime matches the form's -- it also needs a fresh render each time,
	// since a Turnstile token is single-use.
	function renderTurnstile() {
		if (!browser || !turnstileContainer) return;
		const turnstile = (window as typeof window & { turnstile?: TurnstileGlobal }).turnstile;
		if (!turnstile) return;
		turnstileWidgetId = turnstile.render(turnstileContainer, {
			sitekey: PUBLIC_BUG_REPORT_TURNSTILE_SITE_KEY,
			callback: (token: string) => (turnstileToken = token),
			'expired-callback': () => (turnstileToken = ''),
			'error-callback': () => (turnstileToken = '')
		});
	}

	function loadTurnstileScript(): Promise<void> {
		if (!browser) return Promise.resolve();
		if ((window as typeof window & { turnstile?: unknown }).turnstile) return Promise.resolve();
		const existing = document.querySelector<HTMLScriptElement>('script[data-turnstile]');
		if (existing) {
			return new Promise((resolve) =>
				existing.addEventListener('load', () => resolve(), { once: true })
			);
		}
		return new Promise((resolve) => {
			const script = document.createElement('script');
			script.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js';
			script.async = true;
			script.defer = true;
			script.dataset.turnstile = 'true';
			script.addEventListener('load', () => resolve(), { once: true });
			document.head.appendChild(script);
		});
	}

	$effect(() => {
		if (!open) {
			resetForm();
			return;
		}
		(async () => {
			await loadTurnstileScript();
			renderTurnstile();
		})();
	});

	async function handleSubmit(e: Event) {
		e.preventDefault();
		if (!turnstileToken) {
			submitError = 'Please complete the verification challenge.';
			return;
		}
		isSubmitting = true;
		submitError = null;
		try {
			const response = await fetch('/api/report-bug', {
				method: 'POST',
				headers: { 'content-type': 'application/json' },
				body: JSON.stringify({
					whatIsWrong,
					profile,
					correction,
					turnstileToken,
					questionId,
					questionTitle,
					questionUrl: browser ? page.url.href : ''
				})
			});
			if (!response.ok) {
				throw new Error('submit_failed');
			}
			const result = (await response.json()) as { issueUrl: string };
			issueUrl = result.issueUrl;
		} catch {
			submitError = 'Could not submit the report. Please try again.';
			const turnstile = (window as typeof window & { turnstile?: TurnstileGlobal }).turnstile;
			if (turnstile && turnstileWidgetId) turnstile.reset(turnstileWidgetId);
			turnstileToken = '';
		} finally {
			isSubmitting = false;
		}
	}
</script>

<Dialog.Root bind:open>
	<Dialog.Content class="max-w-md">
		<Dialog.Title>Report a bug</Dialog.Title>
		<Dialog.Description class="mb-4">
			Something wrong with this question? Let us know and we'll take a look.
		</Dialog.Description>

		{#if issueUrl}
			<div class="flex flex-col items-center gap-3 py-4 text-center">
				<CheckCircle2 class="size-8 text-green-600 dark:text-green-400" />
				<p class="text-sm text-muted-foreground">
					Thanks, your report has been filed. You can
					<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -- external GitHub URL, not an app route -->
					<a
						href={issueUrl}
						target="_blank"
						rel="noopener noreferrer"
						class="text-primary underline">track it here</a
					>.
				</p>
				<Button variant="outline" size="sm" onclick={() => (open = false)}>Close</Button>
			</div>
		{:else}
			<form class="flex flex-col gap-3" onsubmit={handleSubmit}>
				<div class="flex flex-col gap-1.5">
					<label for="report-bug-what" class="text-xs font-medium text-muted-foreground"
						>What is wrong</label
					>
					<Textarea
						id="report-bug-what"
						required
						rows={3}
						bind:value={whatIsWrong}
						placeholder="Describe what's broken or incorrect"
					/>
				</div>
				<div class="flex flex-col gap-1.5">
					<label for="report-bug-profile" class="text-xs font-medium text-muted-foreground"
						>Your LinkedIn/X profile</label
					>
					<Input
						id="report-bug-profile"
						required
						bind:value={profile}
						placeholder="linkedin.com/in/you or x.com/you"
					/>
				</div>
				<div class="flex flex-col gap-1.5">
					<label for="report-bug-correction" class="text-xs font-medium text-muted-foreground"
						>What should be the correction</label
					>
					<Textarea
						id="report-bug-correction"
						required
						rows={3}
						bind:value={correction}
						placeholder="What should it say or do instead"
					/>
				</div>

				<div bind:this={turnstileContainer}></div>

				{#if submitError}
					<p class="text-sm text-destructive">{submitError}</p>
				{/if}

				<Button type="submit" disabled={isSubmitting} class="w-full">
					{isSubmitting ? 'Submitting...' : 'Submit report'}
				</Button>
			</form>
		{/if}
	</Dialog.Content>
</Dialog.Root>
