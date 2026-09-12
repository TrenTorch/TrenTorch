<script lang="ts">
	import { resolve } from '$app/paths';
	import * as Avatar from '$lib/components/ui/avatar';
</script>

<a
	href={resolve('/account')}
	class="inline-flex size-9 items-center justify-center rounded-md transition-colors hover:bg-accent hover:text-accent-foreground"
	aria-label="Your account"
>
	<Avatar.Root class="size-7">
		<Avatar.Fallback class="font-mono text-xs">?</Avatar.Fallback>
	</Avatar.Root>
</a>
