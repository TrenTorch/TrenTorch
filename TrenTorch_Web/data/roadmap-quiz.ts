export interface QuizQuestion {
	// Names the real curriculum question this is inspired by, for
	// traceability/analytics only -- prompt/options below are a reworded,
	// concrete-instance variant, never verbatim text from that question, so
	// solving it later in the track never feels like a repeat.
	sourceTitle: string;
	prompt: string;
	options: string[];
	correctIndex: number;
}

type DomainQuizId = 'ds' | 'ml' | 'dl' | 'nlp' | 'inf';

export const quizBank: Record<'general' | DomainQuizId, QuizQuestion[]> = {
	general: [
		{
			sourceTitle: 'Dot product and vector norms (L1, L2, L-infinity)',
			prompt: 'What is the L2 norm of the vector [3, 4]?',
			options: ['5', '7', '12', '25'],
			correctIndex: 0
		},
		{
			sourceTitle: 'Matrix multiplication from first principles',
			prompt: 'If A is a 3×4 matrix and B is a 4×2 matrix, what is the shape of A @ B?',
			options: ['3×2', '4×4', 'Undefined', '3×4'],
			correctIndex: 0
		},
		{
			sourceTitle: 'Transpose and its effect on shape',
			prompt: 'If M has shape (4, 7), what is the shape of Mᵀ?',
			options: ['(7, 4)', '(4, 7)', '(4, 4)', '(7, 7)'],
			correctIndex: 0
		},
		{
			sourceTitle: 'Broadcasting rules for elementwise operations',
			prompt: 'Can a (3, 1) array and a (3, 4) array be added via NumPy broadcasting?',
			options: [
				'Yes — the size-1 axis stretches to 4',
				'No — shapes must match exactly',
				'Only if both are 1D',
				'Only if you transpose one first'
			],
			correctIndex: 0
		}
	],
	ds: [
		{
			sourceTitle: 'Conditional probability from a joint distribution',
			prompt:
				'P(A) = 0.3, P(B) = 0.4, P(A and B) = 0.12. Are A and B independent, and what is P(A|B)?',
			options: [
				'Independent, P(A|B) = 0.3',
				'Not independent, P(A|B) = 0.12',
				'Not independent, P(A|B) = 0.4',
				'Independent, P(A|B) = 0.12'
			],
			correctIndex: 0
		}
	],
	ml: [
		{
			sourceTitle: 'Bias-variance tradeoff, and why overfitting increases variance',
			prompt: 'As model complexity increases (data held fixed), what typically happens?',
			options: [
				'Variance increases, bias decreases',
				'Variance decreases, bias increases',
				'Both increase',
				'Both decrease'
			],
			correctIndex: 0
		}
	],
	dl: [
		{
			sourceTitle: 'Jacobian: the matrix of all partial derivatives of a vector-valued function',
			prompt: 'For f: R³ → R², what are the dimensions of the Jacobian matrix?',
			options: ['2×3', '3×2', '3×3', '2×2'],
			correctIndex: 0
		}
	],
	nlp: [
		{
			sourceTitle: 'Scaled dot-product attention, the formula behind QK^T',
			prompt: 'In scaled dot-product attention, why divide QK^T by √d_k?',
			options: [
				'Keeps softmax gradients well-scaled as d_k grows',
				'Normalizes values into [0,1]',
				'Makes Q and K orthogonal',
				'Reduces parameter count'
			],
			correctIndex: 0
		}
	],
	inf: [
		{
			sourceTitle: 'Time complexity of naive matrix multiplication',
			prompt:
				'What is the time complexity of naive (triple-loop) multiplication of two n×n matrices?',
			options: ['O(n³)', 'O(n²)', 'O(n log n)', 'O(n)'],
			correctIndex: 0
		}
	]
};

// Every selected domain contributes exactly one question on top of the 2
// baseline "general" questions everyone gets -- quiz length scales directly
// with how much ground needs covering (2 + number of domains picked).
export function assembleQuiz(selectedDomainIds: string[]): QuizQuestion[] {
	const quiz = [...quizBank.general];
	for (const id of selectedDomainIds) {
		if (id in quizBank && id !== 'general') {
			quiz.push(...quizBank[id as DomainQuizId]);
		}
	}
	return quiz;
}
