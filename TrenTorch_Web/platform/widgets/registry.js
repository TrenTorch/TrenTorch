// Maps a README frontmatter `widget:` id to its module. Written as an
// explicit map (not a computed path) so bundlers can statically analyze
// and code-split each import -- a widget's JS only ever loads for a
// question that actually uses it.
//
// Every module here exports `mount(root)`, which wires up the widget's
// DOM (already present -- it's raw HTML embedded directly in the
// question's Theory markdown) and returns a cleanup function.
export const widgetRegistry = {
	'gaussian-distribution': () => import('./gaussian-distribution.js'),
	'row-reduction-stepper': () => import('./row-reduction-stepper.js'),
	'vector-orthogonalization-animator': () => import('./vector-orthogonalization-animator.js'),
	'taylor-approximation': () => import('./taylor-approximation.js'),
	'gradient-descent-playground': () => import('./gradient-descent-playground.js')
};
