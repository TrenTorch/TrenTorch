/* eslint-disable @typescript-eslint/no-explicit-any */
// plotly.js is 4.8 MB, so it is not part of the app bundle: it is a static file
// (platform/static/vendor/, checksummed in vendor.json) that is loaded by a script tag
// the first time a plotly chart has to be drawn. The service worker caches it after
// that, so it is a one-time download and works offline.
export const PLOTLY_JS = 'plotly-4.1.1.min.js';

let loading: Promise<any> | null = null;

export function loadPlotly(): Promise<any> {
	const existing = (globalThis as any).Plotly;
	if (existing) return Promise.resolve(existing);
	loading ??= new Promise((resolve, reject) => {
		const script = document.createElement('script');
		script.src = `/vendor/${PLOTLY_JS}`;
		script.async = true;
		script.onload = () => resolve((globalThis as any).Plotly);
		script.onerror = () => {
			loading = null;
			script.remove();
			reject(new Error('Could not load plotly.js'));
		};
		document.head.appendChild(script);
	});
	return loading;
}
