export const CLAIMS = {
	freePractice: {
		live: true,
		text: 'a free machine-learning practice platform with no subscription or paid tier',
		shortText: 'free ML practice'
	},
	sourceAvailability: {
		live: true,
		text: 'available under the PolyForm Noncommercial License 1.0.0 for noncommercial use',
		shortText: 'source-available under a noncommercial license'
	},
	fromScratch: {
		live: true,
		text: 'implement machine-learning algorithms from scratch, from first principles, in Python',
		shortText: 'first-principles Python'
	},
	pytorchStyleImplementations: {
		live: true,
		text: 'practice the tensor operations, layers, optimizers, and transformer components behind PyTorch',
		shortText: 'PyTorch-style implementations'
	},
	hiddenTestGrading: {
		live: true,
		text: 'get instant grading against hidden tests for Python coding problems in your browser',
		shortText: 'hidden-test grading'
	},
	browserPythonRuntime: {
		live: true,
		text: 'run Python code in your browser without installing a local GPU runtime',
		shortText: 'browser-based Python'
	},
	cudaTritonConcepts: {
		live: true,
		text: 'learn CUDA and Triton kernel concepts from first principles without compiling arbitrary CUDA C in the browser',
		shortText: 'CUDA and Triton concepts'
	},
	inferenceSystems: {
		live: true,
		text: 'practice machine-learning inference, systems, and kernel concepts',
		shortText: 'inference and systems practice'
	},
	curriculumCoverage: {
		live: true,
		text: 'math and statistics, data science foundations, classical and deep learning, NLP, transformers and LLMs, computer vision, reinforcement learning, inference, and ML systems including CUDA and Triton kernel concepts',
		shortText: 'deep learning, data science, statistics, inference, CUDA/Triton'
	},
	dailyRatedProblem: {
		live: true,
		text: 'take on a daily Problem of the Day with ratings',
		shortText: 'daily rated problems'
	},
	appliedPotdScenarios: {
		live: true,
		text: 'solve applied, case-based coding prompts in the Problem of the Day',
		shortText: 'case-based daily problems'
	},
	selectedVisualizations: {
		live: true,
		text: 'explore selected math and systems topics with interactive visualizations',
		shortText: 'selected interactive visualizations'
	},
	researchPaperImplementations: {
		live: false,
		text: 'implement techniques directly from research papers',
		shortText: 'research-paper implementations'
	}
} as const;

export type ClaimKey = keyof typeof CLAIMS;

export function getLiveClaimText(keys: readonly ClaimKey[]): string[] {
	return keys.flatMap((key) => (CLAIMS[key].live ? [CLAIMS[key].text] : []));
}
