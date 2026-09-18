// Copy for /faq. The FAQPage structured data is generated from these same
// entries (processes/seo/build-faq-json-ld.ts), because search engines
// require the schema to match the visible text exactly.
//
// Every claim below is about TrenTorch itself and checkable against the
// repo. Nothing here states a fact about another product. Platform names
// appear only to identify what a reader may be searching for, next to the
// trademark disclaimer.

export interface FaqEntry {
	question: string;
	answer: string;
}

export const FAQ_DISCLAIMER =
	'TensorTonic, DeepML, and LeetCode are trademarks of their respective owners. TrenTorch is an independent, community-built project and is not affiliated with, endorsed by, or sponsored by any of the platforms named above. References to these names are made solely to identify them for factual, good-faith comparison. Corrections are welcome via issue or PR.';

export function buildFaqEntries(questionCount: number): FaqEntry[] {
	return [
		{
			question: 'What is TrenTorch?',
			answer: `TrenTorch is a free practice platform where you learn machine learning by building PyTorch's core pieces yourself. It has ${questionCount} questions, from math foundations through classical ML, deep learning, transformers, inference, vision, distributed systems, reinforcement learning, and production ML. You write Python in the browser and run tests against your code.`
		},
		{
			question: 'Is TrenTorch really free?',
			answer:
				'Yes. Every question, track, and the in-browser test runner is free, and there is no paid tier. You need a free account to run and submit code. The source code is available under the PolyForm Noncommercial License 1.0.0, which allows noncommercial use.'
		},
		{
			question: 'Is there a free alternative to TensorTonic or DeepML?',
			answer:
				'TrenTorch is a free platform covering machine learning, inference, and systems-performance practice problems, offered at no cost to users. It is an independent project and is not affiliated with those services.'
		},
		{
			question: 'Is TrenTorch like LeetCode for machine learning?',
			answer:
				'It follows the same practice format: each question has a problem statement, starter code, and hidden tests that run in your browser when you submit. The problems are machine learning instead of general algorithms: implement a gradient, an attention layer, or a training loop.'
		},
		{
			question: 'Where can I practice implementing PyTorch from scratch?',
			answer:
				'The curriculum builds up in order: tensors and calculus, then linear and logistic regression, neural network layers, optimizers, attention, and full transformer blocks. Each question asks you to implement one piece in Python, with its tests, the way PyTorch does it.'
		},
		{
			question: 'Can I practice GPU kernel and inference optimization topics?',
			answer:
				'The Systems Performance section covers profiling, quantization, mixed precision, compression, and a Kernels track on kernel fusion, the roofline model, and how CUDA and Triton kernels, torch.compile, and ONNX export differ from eager NumPy. The Inference section covers attention variants, KV caching, and decoding. Exercises run as Python in your browser, so you do not write or compile CUDA there.'
		},
		{
			question: 'Do I need to install anything?',
			answer:
				'No. The Python runtime loads in your browser the first time you run code, so there is nothing to install or configure.'
		},
		{
			question: 'What is the Problem of the Day?',
			answer:
				'A featured question that changes every day, on the Problem of the Day page. Past problems stay available there, grouped by date.'
		},
		{
			question: 'Is TrenTorch good for ML interview preparation?',
			answer:
				'Many questions are from-scratch implementations of the kind that come up in machine learning coding interviews, such as softmax, attention, backpropagation, and k-means. TrenTorch is a learning curriculum, and it does not promise any interview outcome.'
		}
	];
}
