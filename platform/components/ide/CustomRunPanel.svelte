<script lang="ts">
	import { Play } from '@lucide/svelte';

	let {
		functionNames = [],
		isRunning = false,
		output = '',
		hasError = false,
		onRun = () => {}
	} = $props<{
		functionNames: string[];
		isRunning: boolean;
		output?: string;
		hasError?: boolean;
		onRun?: (functionName: string, argumentsJson: string, expectedJson: string) => void;
	}>();

	let functionName = $state('');
	let argumentsJson = $state('[]');
	let expectedJson = $state('');
	let validationError = $state('');

	$effect(() => {
		if (!functionName && functionNames.length > 0) functionName = functionNames[0];
	});

	function runCustomCase() {
		validationError = '';
		if (!functionName.trim()) {
			validationError = 'Enter the name of a function in your code.';
			return;
		}
		try {
			const args: unknown = JSON.parse(argumentsJson);
			if (!Array.isArray(args)) {
				validationError = 'Arguments must be a JSON array, such as [2, 3].';
				return;
			}
			if (expectedJson.trim()) JSON.parse(expectedJson);
			onRun(functionName.trim(), argumentsJson, expectedJson);
		} catch (error) {
			validationError = error instanceof Error ? error.message : String(error);
			return;
		}
	}
</script>

<div
	class="flex h-full min-h-0 flex-col gap-3 overflow-y-auto bg-background p-3 font-mono text-xs text-foreground"
>
	<div>
		<h2 class="font-semibold">Custom function input</h2>
		<p class="mt-1 text-muted-foreground">
			Call a function with your own arguments. Add an expected JSON result to check it too.
		</p>
	</div>

	<label class="flex flex-col gap-1">
		<span class="text-muted-foreground">Function name</span>
		<input
			bind:value={functionName}
			list="custom-run-function-names"
			class="h-8 rounded border border-border bg-background px-2 text-foreground outline-none focus-visible:ring-2 focus-visible:ring-primary"
			placeholder="function_name"
		/>
		<datalist id="custom-run-function-names">
			{#each functionNames as name (name)}
				<option value={name}></option>
			{/each}
		</datalist>
	</label>

	<label class="flex min-h-20 flex-1 flex-col gap-1">
		<span class="text-muted-foreground">Positional arguments (JSON array)</span>
		<textarea
			bind:value={argumentsJson}
			class="min-h-16 flex-1 resize-y rounded border border-border bg-background p-2 font-mono text-foreground outline-none focus-visible:ring-2 focus-visible:ring-primary"
			spellcheck="false"
			aria-label="Function arguments as a JSON array"></textarea>
	</label>

	<label class="flex flex-col gap-1">
		<span class="text-muted-foreground">Expected result (optional JSON)</span>
		<input
			bind:value={expectedJson}
			class="h-8 rounded border border-border bg-background px-2 font-mono text-foreground outline-none focus-visible:ring-2 focus-visible:ring-primary"
			placeholder="e.g. 12 or [2, 1]"
			spellcheck="false"
		/>
	</label>

	{#if validationError}
		<p class="text-red-700 dark:text-red-300" role="alert">{validationError}</p>
	{/if}

	<button
		type="button"
		class="inline-flex h-8 items-center justify-center gap-2 self-start rounded bg-primary px-3 font-semibold text-primary-foreground transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
		disabled={isRunning}
		onclick={runCustomCase}
	>
		<Play class="size-3" />
		{isRunning ? 'Running…' : 'Run custom case'}
	</button>
	<p class="text-[10px] text-muted-foreground">
		Custom runs do not count as a submission or change your progress.
	</p>
	{#if output}
		<div class="max-h-[45%] min-h-0 shrink-0 overflow-y-auto border-t border-border pt-3">
			<h3
				class="mb-1 font-semibold {hasError ? 'text-red-700 dark:text-red-300' : 'text-foreground'}"
			>
				Result
			</h3>
			<pre
				class="whitespace-pre-wrap {hasError
					? 'text-red-700 dark:text-red-300'
					: 'text-foreground/80'}">{output}</pre>
		</div>
	{/if}
</div>
