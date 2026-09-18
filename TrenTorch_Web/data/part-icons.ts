import {
	Sigma,
	Database,
	TrendingUp,
	GitBranch,
	Layers,
	Cpu,
	SlidersHorizontal,
	MessageSquare,
	Bot,
	Eye,
	Zap,
	MemoryStick,
	Target,
	Rocket,
	Gauge,
	type LucideIcon
} from '@lucide/svelte';

/** One icon per curriculum Part, keyed by Part.id -- purely presentational
 * (the track-picker cards), kept out of data/questions.ts so that file
 * stays free of any UI-layer import. `Gauge` is the fallback for a Part id
 * this map hasn't been updated for yet, so a newly-added Part still renders
 * something instead of crashing the page. */
const PART_ICONS: Record<string, LucideIcon> = {
	'part-math': Sigma,
	'part-data-foundations': Database,
	'part-classical-linear': TrendingUp,
	'part-classical-trees': GitBranch,
	'part-classical-unsupervised': Layers,
	'part-dl-core': Cpu,
	'part-dl-training': SlidersHorizontal,
	'part-seq-modeling': MessageSquare,
	'part-transformers-llm': Bot,
	'part-vision': Eye,
	'part-systems-perf': Zap,
	'part-systems-distributed': MemoryStick,
	'part-rl-alignment': Target,
	'part-production-ml': Rocket,
	'part-inference': Gauge
};

export function getPartIcon(partId: string): LucideIcon {
	return PART_ICONS[partId] ?? Gauge;
}
