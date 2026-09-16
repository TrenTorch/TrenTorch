export interface DomainDef {
	id: string;
	name: string;
	description: string;
	partIds: string[];
}

// partIds reference real Part.id values from ./questions -- domains map to
// whole Parts (what the rest of the app colloquially calls "tracks" too,
// e.g. the Questions page's "N tracks" copy), not the finer-grained Track
// records nested inside each Part.
export const domainDefs: DomainDef[] = [
	{
		id: 'ds',
		name: 'Data Science',
		description: 'Stats foundations, EDA, experiment design',
		partIds: ['part-data-foundations', 'part-math']
	},
	{
		id: 'ml',
		name: 'Classical ML',
		description: 'Supervised learning: linear models, trees, unsupervised',
		partIds: [
			'part-math',
			'part-classical-linear',
			'part-classical-trees',
			'part-classical-unsupervised'
		]
	},
	{
		id: 'dl',
		name: 'Deep Learning',
		description: 'Core mechanics, training, vision',
		partIds: ['part-math', 'part-dl-core', 'part-dl-training', 'part-vision']
	},
	{
		id: 'nlp',
		name: 'NLP & Transformers',
		description: 'Sequence modeling, attention, LLMs',
		partIds: ['part-math', 'part-seq-modeling', 'part-transformers-llm']
	},
	{
		id: 'inf',
		name: 'Inference',
		description: 'Systems, memory, production serving',
		partIds: [
			'part-systems-perf',
			'part-systems-distributed',
			'part-production-ml',
			'part-inference'
		]
	}
];

// Shown greyed-out/disabled in the domain-picker step -- not modeled as
// DomainDef entries (no partIds) so nothing here can accidentally become
// selectable before the curriculum actually supports it.
export const comingSoonDomains = [
	{ name: 'Reinforcement Learning', description: 'Coming soon' },
	{ name: 'CUDA', description: 'Coming soon' }
];

// v1: only Math & Statistics for ML is skip-eligible, regardless of which
// domains were picked -- a strong placement-quiz score skips straight past
// it, nothing else is ever skipped.
export const SKIP_ELIGIBLE_PART_ID = 'part-math';
