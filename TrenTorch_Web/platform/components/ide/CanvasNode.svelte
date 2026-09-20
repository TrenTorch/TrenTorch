<script lang="ts">
	import { Handle, Position, type NodeProps } from '@xyflow/svelte';
	import {
		Database,
		Zap,
		Globe,
		Layers,
		Clock,
		HardDrive,
		Search,
		CheckCircle2,
		ShieldCheck,
		GitBranch,
		Repeat,
		ListOrdered,
		Split,
		AlertTriangle,
		Lock,
		Eye,
		FileText,
		MessageSquare,
		Brain,
		Route,
		Wrench,
		XCircle,
		ArrowRightCircle,
		Circle
	} from '@lucide/svelte';

	const ICONS: Record<string, typeof Circle> = {
		Database,
		Zap,
		Globe,
		Layers,
		Clock,
		HardDrive,
		Search,
		CheckCircle2,
		ShieldCheck,
		GitBranch,
		Repeat,
		ListOrdered,
		Split,
		AlertTriangle,
		Lock,
		Eye,
		FileText,
		MessageSquare,
		Brain,
		Route,
		Wrench,
		XCircle,
		ArrowRightCircle
	};

	let { data, selected }: NodeProps = $props();
	let Icon = $derived(ICONS[data.icon as string] ?? Circle);
</script>

<div
	class="min-w-44 rounded-lg border-2 bg-neutral-900 px-3 py-2.5 shadow-lg transition-colors {selected
		? 'border-amber-500'
		: 'border-neutral-700'}"
>
	<Handle
		type="target"
		position={Position.Left}
		class="!h-4 !w-4 !border-amber-500 !bg-neutral-900"
	/>
	<div class="flex items-center gap-2">
		<div
			class="flex size-6 shrink-0 items-center justify-center rounded bg-amber-500/15 text-amber-500"
		>
			<Icon class="size-3.5" />
		</div>
		<span class="text-xs font-semibold text-white">{data.label}</span>
	</div>
	{#if data.subtitle}
		<p class="mt-1 pl-8 text-[10px] text-amber-500/80">{data.subtitle}</p>
	{/if}
	<Handle
		type="source"
		position={Position.Right}
		class="!h-4 !w-4 !border-amber-500 !bg-neutral-900"
	/>
</div>
