import {
	Code,
	Sigma,
	Database,
	GitBranch,
	Cpu,
	MessageSquare,
	Target,
	Eye,
	Bot,
	Network,
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
	'part-python': Code,
	'part-mathematics': Sigma,
	'part-data-science': Database,
	'part-classical-ml': GitBranch,
	'part-deep-learning': Cpu,
	'part-language-models': MessageSquare,
	'part-reinforcement-learning': Target,
	'part-computer-vision': Eye,
	'part-agentic-systems': Bot,
	'part-distributed-systems': Network,
	'part-production-reliability': Rocket
};

export function getPartIcon(partId: string): LucideIcon {
	return PART_ICONS[partId] ?? Gauge;
}
