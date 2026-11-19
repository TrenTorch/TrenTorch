<script lang="ts">
	import { checkAnswer, workbook } from '$processes/cuda/model';
	// One calculation-workbook problem: type your number, press Check. The expected value comes from the same
	// model functions the figures use, so a figure and the workbook can never disagree.
	let { problem }: { problem: number } = $props();
	const p = $derived(workbook().find((x) => x.n === problem));
	let given = $state('');
	let verdict = $state<'' | 'right' | 'wrong' | 'bad'>('');
	function check() {
		const v = Number(given.replace(/,/g, ''));
		verdict =
			!p || given.trim() === '' || Number.isNaN(v) ? 'bad' : checkAnswer(p, v) ? 'right' : 'wrong';
	}
</script>

{#if p}
	<form
		class="check"
		onsubmit={(e) => {
			e.preventDefault();
			check();
		}}
	>
		<label>
			Your answer ({p.unit})
			<input type="text" inputmode="decimal" bind:value={given} aria-describedby="g1-{problem}-v" />
		</label>
		<button type="submit">Check</button>
		<span id="g1-{problem}-v" class="v {verdict}" role="status" aria-live="polite">
			{#if verdict === 'right'}✓ Correct{p.tolerance ? ` (within ${p.tolerance * 100}%)` : ''}
			{:else if verdict === 'wrong'}✗ Not quite{p.tolerance
					? ` (the check allows ${p.tolerance * 100}%)`
					: ''}. Re-read the formula and try again, or open the worked answer.
			{:else if verdict === 'bad'}Type a number first.{/if}
		</span>
	</form>
{/if}

<style>
	.check {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.5rem;
		margin: 0.5rem 0;
		font-size: 0.85rem;
	}
	input {
		margin-left: 0.4rem;
		width: 9rem;
		padding: 0.2rem 0.4rem;
		border: 1px solid var(--border);
		border-radius: 0.35rem;
		background: var(--card);
		color: var(--foreground);
	}
	button {
		padding: 0.25rem 0.8rem;
		border: 1px solid var(--border);
		border-radius: 0.4rem;
		background: var(--secondary);
	}
	.right {
		color: #16a34a;
	}
	.wrong,
	.bad {
		color: #dc2626;
	}
</style>
