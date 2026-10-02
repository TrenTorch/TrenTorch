import { competitors } from './competitors';
import { CLAIMS } from '$processes/seo/claims';

// Copy for /faq. The FAQPage structured data is generated from these same
// entries (processes/seo/build-faq-json-ld.ts), because search engines
// require the schema to match the visible text exactly.
//
// TrenTorch claims are backed by the repository; competitor summaries are
// sourced from the official pages linked in data/competitors.ts.

export interface FaqEntry {
	question: string;
	answer: string;
}

export const FAQ_DISCLAIMER =
	'TensorTonic, Deep-ML, LeetCode, and Codeforces are trademarks of their respective owners. TrenTorch is an independent, community-built project and is not affiliated with, endorsed by, or sponsored by any of the platforms named above. References to these names are made solely to identify them for factual, good-faith comparison. Corrections are welcome via issue or PR.';

export function buildFaqEntries(questionCount: number): FaqEntry[] {
	const entries: FaqEntry[] = [
		{
			question: 'What is TrenTorch?',
			answer: `TrenTorch is ${CLAIMS.freePractice.text}. It has ${questionCount} questions covering ${CLAIMS.curriculumCoverage.text}. Learners can ${CLAIMS.fromScratch.text} and ${CLAIMS.hiddenTestGrading.text}.`
		},
		{
			question: 'Is TrenTorch really free?',
			answer: `Yes. TrenTorch is ${CLAIMS.freePractice.text}. A free account is needed to run and submit code. The source code is ${CLAIMS.sourceAvailability.text}.`
		},
		{
			question: 'Is TrenTorch open source?',
			answer: `The source code is ${CLAIMS.sourceAvailability.text}. That license is source-available, not an OSI-approved open-source license.`
		},
		{
			question: 'Is TrenTorch a LeetCode for machine learning?',
			answer: `It offers a machine-learning coding practice format: ${CLAIMS.fromScratch.text}, then ${CLAIMS.hiddenTestGrading.text}. TrenTorch is an independent project and is not affiliated with LeetCode.`
		},
		{
			question: 'Is TrenTorch a Codeforces for machine learning?',
			answer: `TrenTorch offers a daily rated problem loop: ${CLAIMS.dailyRatedProblem.text}. Learners can also ${CLAIMS.appliedPotdScenarios.text}. Its focus is machine-learning implementation rather than general competitive programming, and it is not affiliated with Codeforces.`
		},
		{
			question: 'Can I practice PyTorch concepts from scratch?',
			answer: `Yes. The curriculum includes tensor operations, neural-network layers, optimizers, attention, and transformer components. TrenTorch lets learners ${CLAIMS.pytorchStyleImplementations.text} and ${CLAIMS.fromScratch.text}.`
		},
		{
			question: 'Can I learn CUDA and Triton concepts?',
			answer: `The Systems Performance curriculum includes kernel concepts, and exercises run in Python. TrenTorch helps learners ${CLAIMS.cudaTritonConcepts.text}.`
		},
		{
			question: 'Can I practice ML inference and systems?',
			answer: `Yes. The curriculum includes inference, serving, performance, and kernel topics. Learners can ${CLAIMS.inferenceSystems.text}.`
		},
		{
			question: 'Do I need to install anything or have a GPU?',
			answer: `No local GPU runtime is needed. You can ${CLAIMS.browserPythonRuntime.text}.`
		},
		{
			question: 'What is the Problem of the Day?',
			answer: `The Problem of the Day is a featured daily coding problem. TrenTorch lets learners ${CLAIMS.dailyRatedProblem.text} and ${CLAIMS.appliedPotdScenarios.text}; published problems remain available at their permanent problem pages.`
		},
		{
			question: 'How does TrenTorch grading work?',
			answer: `Submit Python code to run it against hidden tests in the browser. ${CLAIMS.hiddenTestGrading.text}.`
		},
		{
			question: 'Is TrenTorch useful for ML interview practice?',
			answer: `The curriculum includes from-scratch ML implementation practice and coding problems. Learners can ${CLAIMS.fromScratch.text} and ${CLAIMS.hiddenTestGrading.text}. TrenTorch is a learning curriculum and does not promise an interview outcome.`
		}
	];

	if (CLAIMS.researchPaperImplementations.live) {
		entries.push({
			question: 'Can I implement research papers on TrenTorch?',
			answer: `Yes. TrenTorch lets learners ${CLAIMS.researchPaperImplementations.text}.`
		});
	}

	for (const competitor of competitors) {
		entries.push({
			question: `How is TrenTorch different from ${competitor.name}?`,
			answer: `${competitor.summary} TrenTorch focuses on ${CLAIMS.fromScratch.text}, ${CLAIMS.hiddenTestGrading.text}, and ${CLAIMS.dailyRatedProblem.text}. Check the official links on the ${competitor.name} alternative page for the reviewed facts.`
		});
	}

	return entries;
}
