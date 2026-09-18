<script lang="ts">
	import { X as XIcon } from '@lucide/svelte';

	// Real public replies, quoted verbatim, each linking to the actual post
	// so anyone can verify the source themselves -- no embedded widget (no
	// third-party script/tracking loaded, keeps the page as fast as
	// everything else on this site), just the words and a link out.
	const TESTIMONIALS = [
		{
			quote:
				"i'm glad you're making the hard parts accessible. cuda and inference need more hands-on paths like this.",
			name: 'Mena Botrous',
			handle: '@MenaBotrous11',
			url: 'https://x.com/MenaBotrous11/status/2098414375866339780'
		},
		{
			quote: 'I forked this project and am studying it carefully. Thank you for your jobs.',
			name: '胡林江',
			handle: '@hulj13',
			url: 'https://x.com/hulj13/status/2098411277307801872'
		},
		{
			quote: 'Excited for this',
			name: 'Parzival',
			handle: '@0xAech',
			url: 'https://x.com/0xAech/status/2098415536011096424'
		},
		{
			quote:
				'Honestly not a big fan of ML, but thank you for making learning accessible to everyone who are interested to learn these kind of stuff',
			name: ';::;',
			handle: '@spykedev1',
			url: 'https://x.com/spykedev1/status/2099300277295657406'
		},
		{
			quote: 'cool work man Must check out',
			name: 'abhinav',
			handle: '@AbhinavXJ',
			url: 'https://x.com/AbhinavXJ/status/2099366578248937922'
		},
		{
			quote: "Let's goo. Noice man it would help new forks",
			name: 'Athrix ☄️',
			handle: '@athrix_codes',
			url: 'https://x.com/athrix_codes/status/2099409710579642664'
		}
	];
</script>

<div class="container grid gap-4 px-4 sm:grid-cols-2 md:px-6 lg:grid-cols-3">
	{#each TESTIMONIALS as t (t.url)}
		<a
			href={t.url}
			target="_blank"
			rel="noopener noreferrer external"
			class="flex flex-col justify-between gap-4 rounded-md border border-border p-5 transition-colors hover:border-foreground/30 hover:bg-secondary"
		>
			<p class="text-sm text-foreground">&ldquo;{t.quote}&rdquo;</p>
			<div class="flex items-center justify-between gap-2 text-xs text-muted-foreground">
				<span>
					<span class="font-medium text-foreground">{t.name}</span>
					{t.handle}
				</span>
				<XIcon class="size-3.5 shrink-0" aria-hidden="true" />
			</div>
		</a>
	{/each}
</div>
