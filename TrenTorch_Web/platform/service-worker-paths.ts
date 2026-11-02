// Which static files the service worker leaves out of its install-time precache. Kept apart from
// service-worker.ts, which cannot be imported outside a service worker, so the rule can be tested.

// Large files that only some questions need, hosted on this site: the Python wheels and plotly.js. Their
// names carry a version, so a cache hit is always right and they are cached the first time they are fetched.
export const LAZY_SEGMENTS = ['/wheels/', '/vendor/'];
export const isLazyFile = (path: string) => LAZY_SEGMENTS.some((segment) => path.includes(segment));

// In-browser language runtimes (Go, Rust, Java, C++), tens of MB each, fetched by the worker of the language a
// student picks. Their names are not versioned, so they are left to the HTTP cache rather than cached here.
// A new `*-runtime/` folder under static/ must be added here, or every first-time visitor downloads it.
export const RUNTIME_SEGMENTS = [
	'/go-runtime/',
	'/rust-runtime/',
	'/java-runtime/',
	'/cpp-runtime/'
];
export const isRuntimeFile = (path: string) =>
	RUNTIME_SEGMENTS.some((segment) => path.includes(segment));

/** Whether a static file belongs in the precache a new visitor downloads on their first visit. */
export const shouldPrecache = (path: string) => !isLazyFile(path) && !isRuntimeFile(path);
