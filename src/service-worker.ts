/// <reference types="@sveltejs/kit" />
/// <reference lib="webworker" />

// SvelteKit auto-registers this file as the app's service worker. Its only
// job: make the Pyodide runtime (CPython + NumPy + stdlib, ~7.8 MB from
// jsDelivr) a genuine one-time download. jsDelivr already sends
// `immutable, max-age=1y`, but the HTTP cache is evictable and per-cache-
// partition; a dedicated Cache Storage entry survives longer and works
// offline. Every other request passes straight through untouched.

/* eslint-disable @typescript-eslint/no-explicit-any */
const sw = self as any;

const PYODIDE_CACHE = 'pyodide-v0.27.2';
const PYODIDE_ORIGIN = 'https://cdn.jsdelivr.net';
const PYODIDE_PATH = '/pyodide/v0.27.2/';

sw.addEventListener('install', () => sw.skipWaiting());

sw.addEventListener('activate', (event: any) => {
	event.waitUntil(
		(async () => {
			// Drop caches from any older pinned Pyodide version.
			const keys = await caches.keys();
			await Promise.all(
				keys
					.filter((k) => k.startsWith('pyodide-') && k !== PYODIDE_CACHE)
					.map((k) => caches.delete(k))
			);
			await sw.clients.claim();
		})()
	);
});

sw.addEventListener('fetch', (event: any) => {
	const url = new URL(event.request.url);
	const isPyodide =
		url.origin === PYODIDE_ORIGIN &&
		url.pathname.startsWith(PYODIDE_PATH) &&
		event.request.method === 'GET';
	if (!isPyodide) return; // everything else: default network behaviour

	event.respondWith(
		(async () => {
			const cache = await caches.open(PYODIDE_CACHE);
			const hit = await cache.match(event.request);
			if (hit) return hit;
			const res = await fetch(event.request);
			if (res.ok) cache.put(event.request, res.clone());
			return res;
		})()
	);
});

export {};
