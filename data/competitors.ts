export type CompetitorCapability = 'yes' | 'partial' | 'unverified';
export type CompetitorCapabilityField =
	| 'coversFromScratchML'
	| 'coversPyTorch'
	| 'coversCudaTriton'
	| 'coversInferenceServing'
	| 'hasInstantGrading'
	| 'hasDailyProblemAndRating'
	| 'hasInteractiveVisualizations'
	| 'hasResearchPaperImplementations';

export interface Competitor {
	slug: string;
	name: string;
	url: string;
	summary: string;
	coversFromScratchML: CompetitorCapability;
	coversPyTorch: CompetitorCapability;
	coversCudaTriton: CompetitorCapability;
	coversInferenceServing: CompetitorCapability;
	hasInstantGrading: CompetitorCapability;
	hasDailyProblemAndRating: CompetitorCapability;
	hasInteractiveVisualizations: CompetitorCapability;
	hasResearchPaperImplementations: CompetitorCapability;
	capabilityNotes: Partial<Record<CompetitorCapabilityField, string>>;
	pricing: 'free' | 'freemium' | 'paid';
	verifiedOn: string;
	sources: { label: string; url: string }[];
}

export const competitors: Competitor[] = [
	{
		slug: 'tensortonic',
		name: 'TensorTonic',
		url: 'https://www.tensortonic.com/',
		summary:
			'TensorTonic describes its platform as machine-learning practice through code, with from-scratch algorithms, GPU kernels, visualizations, and research implementations. Its homepage lists Python, NumPy, PyTorch, CUDA, and Triton.',
		coversFromScratchML: 'yes',
		coversPyTorch: 'yes',
		coversCudaTriton: 'yes',
		coversInferenceServing: 'yes',
		hasInstantGrading: 'unverified',
		hasDailyProblemAndRating: 'unverified',
		hasInteractiveVisualizations: 'yes',
		hasResearchPaperImplementations: 'yes',
		capabilityNotes: {},
		pricing: 'freemium',
		verifiedOn: '2026-10-02',
		sources: [{ label: 'Official homepage and pricing', url: 'https://www.tensortonic.com/' }]
	},
	{
		slug: 'deep-ml',
		name: 'Deep-ML',
		url: 'https://www.deep-ml.com/',
		summary:
			'Deep-ML describes itself as a machine-learning practice platform with from-scratch coding problems, browser-based Python, test feedback, interactive math visualizations, labs, projects, and learning paths. Its homepage lists PyTorch, CUDA, and Triton problem environments.',
		coversFromScratchML: 'yes',
		coversPyTorch: 'yes',
		coversCudaTriton: 'yes',
		coversInferenceServing: 'unverified',
		hasInstantGrading: 'yes',
		hasDailyProblemAndRating: 'partial',
		hasInteractiveVisualizations: 'yes',
		hasResearchPaperImplementations: 'unverified',
		capabilityNotes: {
			hasDailyProblemAndRating:
				'An official pricing page lists a daily question; a daily problem rating was not confirmed.'
		},
		pricing: 'freemium',
		verifiedOn: '2026-10-02',
		sources: [
			{ label: 'Official homepage', url: 'https://www.deep-ml.com/' },
			{ label: 'Official pricing page', url: 'https://www.deep-ml.com/premium' }
		]
	}
];

export function getCompetitor(slug: string): Competitor | undefined {
	return competitors.find((competitor) => competitor.slug === slug);
}
