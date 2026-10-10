<script lang="ts">
	import { resolve } from '$app/paths';
	import { ArrowRight, Mail } from '@lucide/svelte';
	import LogoBadge from './LogoBadge.svelte';
	import GithubIcon from './GithubIcon.svelte';
	import XIcon from './XIcon.svelte';
	import FooterVoyager from './FooterVoyager.svelte';

	const GITHUB_URL = 'https://github.com/TrenTorch/TrenTorch';
	const X_GROUP_URL = 'https://x.com/i/chat/group_join/g2101356566318608713/x8UvYPX4v3';

	const columns: { title: string; links: { label: string; href: string; external?: boolean }[] }[] =
		[
			{
				title: 'Practice',
				links: [
					{ label: 'Module', href: resolve('/questions') },
					{ label: 'Problem of the day', href: resolve('/potd') }
				]
			},
			{
				title: 'Project',
				links: [
					{ label: 'GitHub', href: GITHUB_URL, external: true },
					{ label: 'X', href: X_GROUP_URL, external: true },
					{ label: 'Contact', href: resolve('/contact') }
				]
			},
			{
				title: 'Legal',
				links: [
					{ label: 'Terms', href: resolve('/terms') },
					{ label: 'Privacy', href: resolve('/privacy') }
				]
			}
		];

	// Visual only for now: no mailing-list backend exists yet, so this never
	// claims a real subscription. It just acknowledges the submit honestly
	// instead of posting anywhere or pretending to succeed.
	let subscribed = $state(false);
	function handleSubscribe(event: SubmitEvent) {
		event.preventDefault();
		subscribed = true;
	}
</script>

<footer class="relative border-t border-border">
	<div class="container pt-12 pb-2 md:px-8">
		<div class="mx-auto max-w-3xl">
			<FooterVoyager />
		</div>
	</div>

	<div class="relative container py-10 md:px-8">
		<div class="grid grid-cols-1 gap-12 lg:grid-cols-[1.3fr_0.8fr_0.8fr_0.7fr_1fr]">
			<div class="flex flex-col gap-4">
				<a href={resolve('/')} class="flex w-fit items-center gap-2.5">
					<LogoBadge class="size-9" />
					<span class="font-mono text-xl leading-none font-bold tracking-wide text-foreground">
						TrenTorch
					</span>
				</a>
				<p class="max-w-xs text-sm leading-relaxed text-muted-foreground">
					Real PyTorch signatures, real internals, scored against real offline PyTorch output.
				</p>
				<a
					href="mailto:engineering@trentorch.com"
					class="flex items-center gap-2 text-sm text-muted-foreground transition-colors hover:text-foreground"
				>
					<Mail class="size-4" />
					engineering@trentorch.com
				</a>
				<div class="flex items-center gap-2">
					<a
						href={GITHUB_URL}
						target="_blank"
						rel="noopener noreferrer"
						aria-label="TrenTorch on GitHub"
						class="flex size-9 items-center justify-center rounded-md border border-border text-muted-foreground transition-colors hover:border-foreground/30 hover:text-foreground"
					>
						<GithubIcon class="size-4" />
					</a>
					<a
						href={X_GROUP_URL}
						target="_blank"
						rel="noopener noreferrer"
						aria-label="TrenTorch on X"
						class="flex size-9 items-center justify-center rounded-md border border-border text-muted-foreground transition-colors hover:border-foreground/30 hover:text-foreground"
					>
						<XIcon class="size-4" />
					</a>
				</div>
			</div>

			{#each columns as column (column.title)}
				<div class="flex flex-col gap-3">
					<h3 class="font-mono text-xs tracking-wider text-foreground uppercase">
						{column.title}
					</h3>
					<nav class="flex flex-col gap-2.5 text-sm text-muted-foreground">
						{#each column.links as link (link.label)}
							{#if link.external}
								<!-- eslint-disable svelte/no-navigation-without-resolve -- external URLs, not app routes -->
								<a
									href={link.href}
									target="_blank"
									rel="noopener noreferrer"
									class="w-fit transition-colors hover:text-foreground"
								>
									{link.label}
								</a>
								<!-- eslint-enable svelte/no-navigation-without-resolve -->
							{:else}
								<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -- already passed through resolve() when `columns` is built -->
								<a href={link.href} class="w-fit transition-colors hover:text-foreground">
									{link.label}
								</a>
							{/if}
						{/each}
					</nav>
				</div>
			{/each}

			<div class="flex flex-col gap-3">
				<h3 class="font-mono text-xs tracking-wider text-foreground uppercase">Stay in the loop</h3>
				<p class="text-sm text-muted-foreground">
					New questions, problem-of-the-day drops, and release notes.
				</p>
				{#if subscribed}
					<p class="text-sm text-foreground">Signups aren't open yet, thanks for the interest.</p>
				{:else}
					<form class="flex gap-2" onsubmit={handleSubscribe}>
						<input
							type="email"
							required
							placeholder="you@example.com"
							aria-label="Email address"
							class="h-9 w-full min-w-0 rounded-md border border-border bg-background px-3 text-sm text-foreground placeholder:text-muted-foreground focus-visible:ring-[3px] focus-visible:ring-ring/50 focus-visible:outline-none"
						/>
						<button
							type="submit"
							aria-label="Subscribe"
							class="flex size-9 shrink-0 items-center justify-center rounded-md bg-primary text-primary-foreground transition-colors hover:bg-primary/90"
						>
							<ArrowRight class="size-4" />
						</button>
					</form>
				{/if}
			</div>
		</div>

		<div class="mt-12 flex flex-col gap-3 border-t border-border pt-6 text-center md:text-left">
			<p class="text-sm leading-loose text-balance text-muted-foreground">
				&copy; {new Date().getFullYear()} TrenTorch. Source-available, free for
				<a
					href="https://github.com/TrenTorch/TrenTorch/blob/TrenTorch-Dev/LICENSE"
					class="font-medium underline underline-offset-4 hover:text-foreground"
				>
					personal and educational use
				</a>
				, and follows a
				<a
					href="https://github.com/TrenTorch/TrenTorch/blob/TrenTorch-Dev/CODE_OF_CONDUCT.md"
					class="font-medium underline underline-offset-4 hover:text-foreground"
				>
					Code of Conduct
				</a>
				.
			</p>

			<!-- Disclaimer for the "Learners signing up from" strip on the landing page -->
			<p class="text-xs leading-relaxed text-balance text-muted-foreground">
				"Learners signing up from" is based on the email domains people used to sign up, counted in
				aggregate; no individual is named. It does not mean these organizations endorse, sponsor, or
				are affiliated with TrenTorch. All names and trademarks belong to their respective owners.
			</p>
		</div>
	</div>
</footer>
