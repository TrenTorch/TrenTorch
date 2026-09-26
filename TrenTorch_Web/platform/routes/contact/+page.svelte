<script lang="ts">
	import { Mail } from '@lucide/svelte';
	import XIcon from '$components/XIcon.svelte';
	import SEO from '$components/SEO.svelte';
	import { withSiteName } from '$processes/seo/with-site-name';

	const X_ACCOUNTS = [
		{ handle: '@Rocky_T07', url: 'https://x.com/Rocky_T07' },
		{ handle: '@ShivtejG236', url: 'https://x.com/ShivtejG236' },
		{ handle: '@aadityansha_06', url: 'https://x.com/aadityansha_06' },
		{ handle: '@maanas_tyagi', url: 'https://x.com/maanas_tyagi' }
	];
</script>

<SEO
	title={withSiteName('Contact')}
	description="Get in touch with the TrenTorch team."
	path="/contact"
/>

<div class="container max-w-3xl px-4 py-12 md:px-6">
	<h1 class="mb-1 font-mono text-2xl font-bold tracking-tight">Contact</h1>
	<p class="mb-8 text-sm text-muted-foreground">
		Found a bug, have feedback, or want to reach out?
	</p>

	<h2 class="mb-3 font-mono text-xs font-semibold tracking-wider text-muted-foreground uppercase">
		Team Mail
	</h2>
	<a
		href="mailto:engineering@trentorch.com"
		class="mb-8 flex items-center gap-3 rounded-md border border-border p-4 transition-colors hover:border-foreground/30 hover:bg-secondary"
	>
		<span
			class="flex size-9 shrink-0 items-center justify-center rounded-md border border-border bg-secondary"
		>
			<Mail class="size-4 text-foreground/80" aria-hidden="true" />
		</span>
		<span class="font-medium">engineering@trentorch.com</span>
	</a>

	<h2
		class="mb-3 inline-flex items-center gap-1.5 font-mono text-xs font-semibold tracking-wider text-muted-foreground uppercase"
	>
		Follow us on <XIcon class="size-3 text-foreground/80" aria-hidden="true" />
	</h2>
	<div class="grid gap-3 sm:grid-cols-2">
		{#each X_ACCOUNTS as account (account.url)}
			<a
				href={account.url}
				target="_blank"
				rel="noopener noreferrer external"
				class="flex items-center gap-3 rounded-md border border-border p-4 transition-colors hover:border-foreground/30 hover:bg-secondary"
			>
				<span
					class="flex size-9 shrink-0 items-center justify-center rounded-full border border-border bg-secondary"
				>
					<XIcon class="size-4 text-foreground/80" aria-hidden="true" />
				</span>
				<span class="font-medium">{account.handle}</span>
			</a>
		{/each}
	</div>
</div>
