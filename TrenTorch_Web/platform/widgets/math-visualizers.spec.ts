import { describe, expect, it } from 'vitest';
import curriculum from '../../data/curriculum/generated-curriculum.json';
import { seededRandom } from '../components/visualizers/seededRandom.js';
import { mathVisualizerIds } from './math-visualizer-ids.js';
import { mathVisualizerIds as configuredVisualizerIds } from './math-visualizers.js';

const questions = curriculum.roots.flatMap((root) =>
	root.sections.flatMap((section) => section.tracks.flatMap((track) => track.questions))
);

// A visualizer is reached either by its own question id, or, when several
// topics were merged into one question, by a `data-widget` placeholder in that
// question's Theory.
const curriculumIds = new Set([
	...questions.map((question) => question.id),
	...questions.flatMap((question) =>
		Array.from(question.theoryMarkdown.matchAll(/data-widget="([^"]+)"/g), (match) => match[1])
	)
]);

describe('math visualizer registry', () => {
	it('covers the brief and every visualizer slug is a question or embedded in one', () => {
		expect(mathVisualizerIds).toHaveLength(47);
		expect(new Set(mathVisualizerIds).size).toBe(mathVisualizerIds.length);
		expect(mathVisualizerIds.filter((id) => !curriculumIds.has(id))).toEqual([]);
		expect(configuredVisualizerIds).toEqual(mathVisualizerIds);
	});

	it('produces repeatable random sequences from the same seed', () => {
		const first = seededRandom(42);
		const second = seededRandom(42);
		expect(Array.from({ length: 5 }, first)).toEqual(Array.from({ length: 5 }, second));
	});
});
