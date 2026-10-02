import type { ClaimKey } from '$processes/seo/claims';

export interface SeoLandingPage {
	slug: string;
	title: string;
	primaryIntent: string;
	partIds: string[];
	claimKeys: ClaimKey[];
	faqs: {
		question: string;
		answerLead: string;
		claimKeys: ClaimKey[];
	}[];
}

export const seoLandingPages: SeoLandingPage[] = [
	{
		slug: 'machine-learning-coding-practice',
		title: 'Free Machine-Learning Coding Practice',
		primaryIntent: 'machine-learning coding practice and coding problems',
		partIds: [
			'part-math',
			'part-classical-linear',
			'part-classical-trees',
			'part-classical-unsupervised',
			'part-dl-core',
			'part-dl-training',
			'part-seq-modeling',
			'part-transformers-llm',
			'part-inference',
			'part-vision',
			'part-systems-perf',
			'part-systems-distributed',
			'part-rl-alignment',
			'part-production-ml'
		],
		claimKeys: [
			'freePractice',
			'fromScratch',
			'hiddenTestGrading',
			'dailyRatedProblem',
			'appliedPotdScenarios',
			'inferenceSystems'
		],
		faqs: [
			{
				question: 'What kind of machine-learning coding practice is available?',
				answerLead:
					'The curriculum links below show the actual topics and problems. TrenTorch lets learners',
				claimKeys: ['fromScratch', 'hiddenTestGrading']
			},
			{
				question: 'Is this like LeetCode or Codeforces for machine learning?',
				answerLead:
					'TrenTorch is an independent machine-learning practice platform where learners can',
				claimKeys: ['fromScratch', 'hiddenTestGrading', 'dailyRatedProblem']
			}
		]
	},
	{
		slug: 'machine-learning-from-scratch',
		title: 'Machine Learning From Scratch in Python',
		primaryIntent: 'machine-learning algorithms from scratch',
		partIds: [
			'part-math',
			'part-classical-linear',
			'part-classical-trees',
			'part-classical-unsupervised',
			'part-dl-core',
			'part-dl-training',
			'part-seq-modeling',
			'part-transformers-llm',
			'part-rl-alignment'
		],
		claimKeys: ['fromScratch', 'hiddenTestGrading', 'pytorchStyleImplementations'],
		faqs: [
			{
				question: 'What does “from scratch” mean on TrenTorch?',
				answerLead:
					'The linked curriculum sections contain the actual implementation problems. Learners',
				claimKeys: ['fromScratch', 'pytorchStyleImplementations']
			}
		]
	},
	{
		slug: 'pytorch-from-scratch',
		title: 'PyTorch Concepts and Implementations From Scratch',
		primaryIntent: 'PyTorch implementation practice',
		partIds: [
			'part-numpy',
			'part-dl-core',
			'part-dl-training',
			'part-seq-modeling',
			'part-transformers-llm',
			'part-vision'
		],
		claimKeys: ['pytorchStyleImplementations', 'fromScratch', 'hiddenTestGrading'],
		faqs: [
			{
				question: 'Can I practice PyTorch concepts from scratch?',
				answerLead:
					'The linked sections include tensor, layer, optimizer, and model-building problems. TrenTorch offers practice to',
				claimKeys: ['pytorchStyleImplementations', 'fromScratch']
			}
		]
	},
	{
		slug: 'ml-inference-practice',
		title: 'Machine-Learning Inference and Systems Practice',
		primaryIntent: 'ML inference and systems coding practice',
		partIds: [
			'part-inference',
			'part-systems-perf',
			'part-systems-distributed',
			'part-production-ml',
			'part-production-and-advanced-ai-systems'
		],
		claimKeys: ['inferenceSystems', 'cudaTritonConcepts', 'hiddenTestGrading'],
		faqs: [
			{
				question: 'What inference and systems topics can I practice?',
				answerLead:
					'Browse the linked sections for the actual curriculum. TrenTorch provides opportunities to',
				claimKeys: ['inferenceSystems', 'cudaTritonConcepts']
			}
		]
	},
	{
		slug: 'ml-kernel-practice',
		title: 'ML Kernel Practice: CUDA and Triton Concepts',
		primaryIntent: 'machine-learning kernel practice',
		partIds: ['part-systems-perf', 'part-inference'],
		claimKeys: ['cudaTritonConcepts', 'inferenceSystems', 'hiddenTestGrading'],
		faqs: [
			{
				question: 'Can I run CUDA or Triton kernels in the browser?',
				answerLead: 'The browser runner uses Python. TrenTorch helps learners',
				claimKeys: ['cudaTritonConcepts']
			}
		]
	},
	{
		slug: 'machine-learning-math-practice',
		title: 'Math and Statistics Practice for Machine Learning',
		primaryIntent: 'machine-learning math and statistics practice',
		partIds: ['part-math', 'part-numpy'],
		claimKeys: ['fromScratch', 'selectedVisualizations', 'hiddenTestGrading'],
		faqs: [
			{
				question: 'Which math topics support the machine-learning curriculum?',
				answerLead:
					'The linked math and NumPy sections show the current coverage. Selected topics can be explored with',
				claimKeys: ['selectedVisualizations']
			}
		]
	},
	{
		slug: 'ml-interview-coding-practice',
		title: 'Machine-Learning Interview Coding Practice',
		primaryIntent: 'machine-learning interview coding practice',
		partIds: [
			'part-classical-linear',
			'part-classical-trees',
			'part-classical-unsupervised',
			'part-dl-core',
			'part-dl-training',
			'part-transformers-llm',
			'part-inference',
			'part-vision'
		],
		claimKeys: ['fromScratch', 'hiddenTestGrading', 'dailyRatedProblem'],
		faqs: [
			{
				question: 'Does TrenTorch guarantee interview outcomes?',
				answerLead: 'No. TrenTorch is a learning and practice platform. Learners can',
				claimKeys: ['fromScratch', 'hiddenTestGrading']
			}
		]
	}
];

export function getSeoLandingPage(slug: string): SeoLandingPage | undefined {
	return seoLandingPages.find((page) => page.slug === slug);
}

export function getSeoLandingPagesForPart(partId: string): SeoLandingPage[] {
	return seoLandingPages.filter((page) => page.partIds.includes(partId));
}
