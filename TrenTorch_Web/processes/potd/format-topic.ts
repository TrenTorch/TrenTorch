// A question's tags are kebab-case ids ('linear-algebra'); the banner shows the
// first one as a readable topic ('Linear Algebra').
const SPECIAL: Record<string, string> = {
	ml: 'ML',
	nlp: 'NLP',
	mlops: 'MLOps',
	svm: 'SVM',
	ai: 'AI',
	llm: 'LLM',
	gpu: 'GPU',
	cnn: 'CNN',
	rnn: 'RNN',
	rl: 'RL',
	sql: 'SQL'
};

export function formatTopic(tag: string): string {
	return tag
		.split('-')
		.filter(Boolean)
		.map((word) => SPECIAL[word] ?? word[0].toUpperCase() + word.slice(1))
		.join(' ');
}
