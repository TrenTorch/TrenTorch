import { describe, it, expect } from 'vitest';
import { questionsById } from './curriculum-index';
import { buildTestHarness } from './build-test-harness';

describe('buildTestHarness', () => {
	it('resolves a cross-track load_solution dependency (regression: adaboost depending on decision-trees)', () => {
		// ensembles-adaboost (01-classical-ml/04-ensembles) depends on
		// 03-decision-trees/03-best-split-minimal-tree's build_tree/
		// predict_tree -- a DIFFERENT track under the same section. This
		// used to crash with `RuntimeError: Missing track-mate dependency
		// '03-best-split-minimal-tree'` because dependency resolution was
		// scoped to the current question's own track and keyed by bare
		// folder name, even though the folder name alone is only unique
		// within one track (see curriculum-index.ts's questionsByFullPath
		// comment).
		const question = questionsById.get('ensembles-adaboost');
		expect(question).toBeDefined();

		const harness = buildTestHarness(question!);

		expect(harness).not.toContain('Missing dependency');
		expect(harness).not.toContain('Missing track-mate dependency');
		expect(harness).toContain('def build_tree');
		expect(harness).toContain('def predict_tree');
	});

	it('still resolves same-track dependencies correctly', () => {
		// 02-classification/05-training-loop depends on both a same-track
		// dependency (01-sigmoid, 03-bce-gradient) and cross-track ones
		// (01-linear-regression/01-hypothesis-function, 04-gd-step) --
		// exercises both paths through the same lookup.
		const question = questionsById.get('classification-training-loop');
		expect(question).toBeDefined();

		const harness = buildTestHarness(question!);

		expect(harness).not.toContain('Missing dependency');
		expect(harness).toContain('def sigmoid');
		expect(harness).toContain('def linear');
	});
});
