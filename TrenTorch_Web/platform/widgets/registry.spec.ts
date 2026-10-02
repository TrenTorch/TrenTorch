import { describe, expect, it } from 'vitest';
import curriculum from '../../data/curriculum/generated-curriculum.json';
import { embeddedWidgetIds, widgetRegistry } from './registry.js';

const questions = curriculum.roots.flatMap((root) =>
	root.sections.flatMap((section) => section.tracks.flatMap((track) => track.questions))
);

describe('embedded widget placeholders', () => {
	it('lists each registered id once, in document order', () => {
		const markdown = [
			'<div class="tt-widget" data-widget="math-independence"></div>',
			'<div class="tt-widget" data-widget="math-bayes-theorem"></div>',
			'<div class="tt-widget" data-widget="math-independence"></div>',
			'<div class="tt-widget" data-widget="not-a-widget"></div>'
		].join('\n\n');
		expect(embeddedWidgetIds(markdown)).toEqual(['math-independence', 'math-bayes-theorem']);
	});

	it('finds nothing in markdown without placeholders', () => {
		expect(embeddedWidgetIds('Just text.')).toEqual([]);
	});

	it('gives a merged question one visualizer per topic', () => {
		const merged = questions.find((q) => q.id === 'math-conditional-probability-bayes');
		expect(embeddedWidgetIds(merged?.theoryMarkdown ?? '')).toEqual([
			'math-conditional-probability',
			'math-chain-rule-of-probability',
			'math-bayes-theorem'
		]);
	});

	it('only references registered widgets, so a typo cannot silently hide a demo', () => {
		const unknown = questions.flatMap((q) =>
			Array.from(q.theoryMarkdown.matchAll(/data-widget="([^"]+)"/g), (m) => m[1])
				.filter((id) => !(id in widgetRegistry))
				.map((id) => `${q.id}: ${id}`)
		);
		expect(unknown).toEqual([]);
	});
});
