import { mathVisualizerIds } from './math-visualizer-ids.js';
import { systemsVisualizerIds as systemsIds } from './systems-visualizer-ids.js';
import { classicalMLVisualizerIds } from './classical-ml-visualizer-ids.js';

// Maps a README frontmatter `widget:` id to its module. Written as an
// explicit map (not a computed path) so bundlers can statically analyze
// and code-split each import -- a widget's JS only ever loads for a
// question that actually uses it.
//
// Every module exports `mount(root)`, which wires up its Theory-tab root
// and returns a cleanup function. Math widgets create their root in
// GuidePane; authored widgets use raw HTML embedded in Theory markdown.
const mathVisualizerLoader = () => import('./math-visualizers.js');
const systemsVisualizerLoader = () => import('./systems-inference-visualizers.js');
const classicalMLVisualizerLoader = () => import('./classical-ml-visualizers.js');

export const widgetRegistry = {
	'gaussian-distribution': () => import('./gaussian-distribution.js'),
	'row-reduction-stepper': () => import('./row-reduction-stepper.js'),
	'vector-orthogonalization-animator': () => import('./vector-orthogonalization-animator.js'),
	'taylor-approximation': () => import('./taylor-approximation.js'),
	'gradient-descent-playground': () => import('./gradient-descent-playground.js'),
	'distribution-shape-explorer': () => import('./distribution-shape-explorer.js'),
	...Object.fromEntries(mathVisualizerIds.map((id) => [id, mathVisualizerLoader])),
	...Object.fromEntries(systemsIds.map((id) => [id, systemsVisualizerLoader])),
	...Object.fromEntries(classicalMLVisualizerIds.map((id) => [id, classicalMLVisualizerLoader]))
};

export const mathVisualizerIdSet = new Set(mathVisualizerIds);
export const systemsVisualizerIdSet = new Set(systemsIds);
export const classicalMLVisualizerIdSet = new Set(classicalMLVisualizerIds);

/**
 * Widget ids embedded in a question's Theory markdown as
 * `<div data-widget="<id>">` placeholders, in order and without repeats.
 * A question that merges several topics uses one placeholder per topic so
 * each keeps its own visualizer. Ids that are not registered are ignored.
 *
 * @param {string} markdown
 * @returns {string[]}
 */
export function embeddedWidgetIds(markdown) {
	const ids = Array.from(markdown.matchAll(/data-widget="([^"]+)"/g), (match) => match[1]);
	return [...new Set(ids)].filter((id) => id in widgetRegistry);
}
