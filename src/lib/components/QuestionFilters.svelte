<script lang="ts">
	import { Input } from '$lib/components/ui/input';
	import * as Select from '$lib/components/ui/select';
	import { Search } from '@lucide/svelte';

	type SolvedFilter = 'all' | 'solved' | 'unsolved';

	let {
		searchQuery = $bindable(''),
		solvedFilter = $bindable<SolvedFilter>('all'),
		topicFilter = $bindable('all'),
		topics
	}: {
		searchQuery: string;
		solvedFilter: SolvedFilter;
		topicFilter: string;
		topics: string[];
	} = $props();

	const solvedLabels: Record<SolvedFilter, string> = {
		all: 'All',
		solved: 'Solved',
		unsolved: 'Unsolved'
	};

	const topicLabel = $derived(topicFilter === 'all' ? 'All topics' : topicFilter);
</script>

<div class="flex flex-col gap-3 sm:flex-row">
	<div class="relative flex-1">
		<Search
			class="pointer-events-none absolute top-1/2 left-2.5 size-4 -translate-y-1/2 text-muted-foreground"
		/>
		<Input type="search" bind:value={searchQuery} placeholder="Search questions" class="pl-8" />
	</div>

	<Select.Root type="single" bind:value={solvedFilter}>
		<Select.Trigger class="w-full sm:w-36">
			{solvedLabels[solvedFilter]}
		</Select.Trigger>
		<Select.Content>
			{#each Object.entries(solvedLabels) as [value, label] (value)}
				<Select.Item {value} {label} />
			{/each}
		</Select.Content>
	</Select.Root>

	<Select.Root type="single" bind:value={topicFilter}>
		<Select.Trigger class="w-full sm:w-48">
			{topicLabel}
		</Select.Trigger>
		<Select.Content>
			<Select.Item value="all" label="All topics" />
			{#each topics as topic (topic)}
				<Select.Item value={topic} label={topic} />
			{/each}
		</Select.Content>
	</Select.Root>
</div>
