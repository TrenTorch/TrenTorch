// in dev, this makes Vite inject its client as this module's first dependency,
// so that global constant replacements are installed before any other module
// (including user hooks) evaluates. In build it's inert.
import.meta.hot;




export { matchers } from './matchers.js';

export const nodes = [
	() => import('./nodes/0'),
	() => import('./nodes/1'),
	() => import('./nodes/2'),
	() => import('./nodes/3'),
	() => import('./nodes/4'),
	() => import('./nodes/5'),
	() => import('./nodes/6'),
	() => import('./nodes/7'),
	() => import('./nodes/8'),
	() => import('./nodes/9'),
	() => import('./nodes/10')
];

export const server_loads = [];

export const dictionary = {
		"/": [2],
		"/account": [3],
		"/contact": [4],
		"/ide/[id]": [5],
		"/potd": [6],
		"/privacy": [7],
		"/questions": [8],
		"/questions/[partId]": [9],
		"/terms": [10]
	};

export const hooks = {
	handleError: (({ error }) => { console.error(error) }),
	
	reroute: (() => {}),
	transport: {}
};

export const decoders = Object.fromEntries(Object.entries(hooks.transport).map(([k, v]) => [k, v.decode]));
export const encoders = Object.fromEntries(Object.entries(hooks.transport).map(([k, v]) => [k, v.encode]));

export const hash = false;

export const decode = (type, value) => decoders[type](value);

export { default as root } from '../root.js';

export const get_error_template = () => import('../shared/error-template.js').then(m => m.default);